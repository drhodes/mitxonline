// @flow
/* global SETTINGS: false */
import React from "react"
import DocumentTitle from "react-document-title"
import { CART_DISPLAY_PAGE_TITLE } from "../../../constants"
import { compose } from "redux"
import { connect } from "react-redux"
import { connectRequest, mutateAsync } from "redux-query"
import { createStructuredSelector } from "reselect"
import { pathOr } from "ramda"

import type { BasketItem, Discount } from "../../../flow/cartTypes"

import Loader from "../../../components/Loader"
import { CartItemCard } from "../../../components/CartItemCard"
import { OrderSummaryCard } from "../../../components/OrderSummaryCard"

import {
  cartQuery,
  cartQueryKey,
  cartSelector,
  totalPriceSelector,
  discountedPriceSelector,
  discountSelector,
  applyDiscountCodeMutation
} from "../../../lib/queries/cart"

import type { RouterHistory } from "react-router"
import { isSuccessResponse } from "../../../lib/util"
import { addUserNotification } from "../../../actions"

type Props = {
  history: RouterHistory,
  cartItems: Array<BasketItem>,
  totalPrice: number,
  discountedPrice: number,
  discounts: Array<Discount>,
  isLoading: boolean,
  applyDiscountCode: (code: string) => Promise<any>,
  addUserNotification: Function,
  forceRequest: Function
}

type CartState = {
  discountCode: string
}

export class CartPage extends React.Component<Props, CartState> {
  state = {
    discountCode: ""
  }

  async addDiscount(ev: Object, { setErrors }: any) {
    const subbedCode = ev.couponCode
    const { applyDiscountCode, forceRequest } = this.props

    this.setState({ discountCode: subbedCode })

    if (String(subbedCode).trim().length === 0) {
      return
    }

    let userMessage

    const resp = await applyDiscountCode(this.state.discountCode)
    if (isSuccessResponse(resp)) {
      userMessage = "Discount code added."

      forceRequest()
    } else {
      userMessage = `Discount code ${this.state.discountCode} is invalid.`

      setErrors({
        couponCode: userMessage
      })
    }
  }
  renderCartItemCard(cartItem: BasketItem) {
    return (
      <CartItemCard
        key={`cartsummarycard_${cartItem.product.id}`}
        product={cartItem.product}
      />
    )
  }

  renderEmptyCartCard() {
    return (
      <div
        className="enrolled-item container card mb-4 rounded-0 flex-grow-1"
        key="cartsummarycard"
      >
        <div className="row d-flex flex-sm-columm p-md-3">
          <div className="flex-grow-1 mx-3 d-sm-flex flex-column">
            <div className="detail">Your cart is empty.</div>
          </div>
        </div>
      </div>
    )
  }

  renderOrderSummaryCard() {
    const { totalPrice, discountedPrice, discounts } = this.props
    const refunds = []

    return (
      <OrderSummaryCard
        totalPrice={totalPrice}
        orderFulfilled={false}
        discountedPrice={discountedPrice}
        discounts={discounts}
        refunds={refunds}
        addDiscount={this.addDiscount.bind(this)}
        discountCode={this.state.discountCode}
      />
    )
  }

  renderFinancialAssistanceOffer() {
    const { cartItems, discounts } = this.props
    let userFlexiblePriceExists = false
    // Check if there are any discounts, and if those discounts are for flexible pricing.
    if (
      discounts &&
      discounts.length > 0 &&
      typeof discounts.find(
        discount => discount.payment_type === "financial-assistance"
      ) !== "undefined"
    ) {
      userFlexiblePriceExists = true
    }

    if (
      cartItems &&
      cartItems.length > 0 &&
      userFlexiblePriceExists === false
    ) {
      if (
        cartItems[0].product &&
        cartItems[0].product.purchasable_object &&
        cartItems[0].product.purchasable_object.course.page &&
        cartItems[0].product.purchasable_object.course.page
          .financial_assistance_form_url
      ) {
        return (
          <a
            href={
              cartItems[0].product.purchasable_object.course.page
                .financial_assistance_form_url
            }
          >
            Need financial assistance?
          </a>
        )
      }
    }
  }

  render() {
    const { cartItems, isLoading } = this.props

    return (
      <DocumentTitle
        title={`${SETTINGS.site_name} | ${CART_DISPLAY_PAGE_TITLE}`}
      >
        <Loader isLoading={isLoading}>
          <div className="std-page-body cart container">
            <div className="row">
              <div className="col-12 d-flex justify-content-between">
                <h1 className="flex-grow-1">Checkout</h1>

                <p className="text-end d-md-none">
                  <a
                    href="https://mitxonline.zendesk.com/hc/en-us"
                    target="_blank"
                    rel="noreferrer"
                  >
                    Help &amp; FAQs
                  </a>
                </p>
              </div>
            </div>
            <div className="row">
              <div className="col-12 d-flex justify-content-end d-md-none">
                <p className="fw-normal">
                  {this.renderFinancialAssistanceOffer()}
                </p>
              </div>
            </div>

            <div className="row d-none d-md-flex mb-3">
              <div className="col-md-6">
                <h4 className="fw-normal">
                  You are about to purchase the following:
                </h4>
              </div>
              <div className="col-md-4 justify-content-end text-end d-flex">
                <h4 className="fw-normal">
                  {this.renderFinancialAssistanceOffer()}
                </h4>
              </div>
              <div className="col-md-2 justify-content-end text-end d-flex">
                <h4 className="fw-normal">
                  <a
                    href="https://mitxonline.zendesk.com/hc/en-us"
                    target="_blank"
                    rel="noreferrer"
                  >
                    Help &amp; FAQs
                  </a>
                </h4>
              </div>
            </div>

            <div className="row d-flex flex-column-reverse flex-md-column flex-lg-row">
              <div className="col-lg-8 enrolled-items">
                {cartItems && cartItems.length > 0
                  ? cartItems.map(this.renderCartItemCard.bind(this))
                  : this.renderEmptyCartCard()}
              </div>
              <div className="col-lg-4">{this.renderOrderSummaryCard()}</div>
            </div>
          </div>
        </Loader>
      </DocumentTitle>
    )
  }
}

const applyDiscountCode = (code: string) =>
  mutateAsync(applyDiscountCodeMutation(code))

const mapStateToProps = createStructuredSelector({
  cartItems:       cartSelector,
  totalPrice:      totalPriceSelector,
  discountedPrice: discountedPriceSelector,
  discounts:       discountSelector,
  isLoading:       pathOr(true, ["queries", cartQueryKey, "isPending"])
})

const mapDispatchToProps = {
  addUserNotification,
  applyDiscountCode
}

const mapPropsToConfig = () => [cartQuery()]

export default compose(
  connect(mapStateToProps, mapDispatchToProps),
  connectRequest(mapPropsToConfig)
)(CartPage)
