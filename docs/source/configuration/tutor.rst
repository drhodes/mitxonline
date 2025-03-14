
Local Open edX Tutor and MITx Online Deployment
===============================================

These instructions describe setting up MITx Online and Tutor from scratch on Linux. These instructions should largely apply to macOS users, and they should also apply to users converting from a devstack-based deployment to Tutor.

..

   These instructions should work for a Tutor Dev or Tutor Nightly deployment as well. Specify ``--tutor-dev`` instead of ``--tutor`` when running ``configure_instance`` so the URLs have a port on them.


At the end of this guide, you should have:


* A fully working MITx Online deployment.
* A working Tutor deployment of edX.
* SSO should work from edX to MITx Online.
* MITx Online should have a service worker set up and should be able to perform tasks using the edX api.
* Tutor's included AuthN MFE should be disabled in favor of the MITx Online authentication system.

Preliminary Steps
-----------------

``pyenv`` (and ``pyenv-virtualenv``\ ) are highly recommended for managing local Python versions. `Use the instructions on their GitHub page to install if you haven't already installed it. <https://github.com/pyenv/pyenv>`_

You'll want to create at least a virtualenv for Tutor. As of this writing, Tutor uses Python 3.8.12 (in the LMS container at least); I have also successfully used 3.9.16. 3.11 has *not* worked for me. You can optionally create a virtualenv for MITx Online too but that's not strictly necessary. (I have one so I can run black/isort/etc. without having to jump into a container to do it.)

Tutor Setup, Part One
---------------------

..

   Note that no hosts file changes are needed if you use the default ``local.overhang.io`` domain - that's a real domain with a wildcard subdomain cname that points to 127.0.0.1.


To begin, you need to follow the `One-Click Installer <https://docs.tutor.overhang.io/quickstart.html>`_ instructions provided by Tutor. Do this with your Tutor virtualenv activated.

..

   Mac/Arm users should instead follow these instructions: `Running Tutor on ARM-based systems <https://docs.tutor.overhang.io/tutorials/arm64.html>`_ It's mostly the same steps that the quickstart does internally, with some changes to rebuild some of the images and flip some dependencies to use compatible images for Arm.


Once Tutor has bootstrapped itself and is available, create a superuser account:

.. code-block::

   tutor local do createuser --staff --superuser edx edx@example.org

Supply a password (the one used by devstack is ``edx`` so use that if you want to be consistent with it). Then, create a service worker account for MITx Online:

.. code-block::

   tutor local do createuser --staff mitx_online_serviceworker service@mitxonline.odl.local

Supply a password (this one doesn't matter for a local deployment, you won't ever actually use the account).

For best results, create two new courses within edX. The MITx Online ``configure_instance`` command expects a couple of courses to exist in edX (because they come with the devstack package):

.. list-table::
   :header-rows: 1

   * - Course ID
     - Course Title
   * - course-v1:edX+DemoX+Demo_Course
     - Demonstration Course
   * - course-v1:edX+E2E-101+course
     - E2E Test Course


If you have a devstack instance handy, you can export these and import them into Tutor. Otherwise, just create them and make sure to set dates for the courses (they default to 2030 otherwise).

Finally, go here to create an access token for the service worker user: http://local.overhang.io/admin/oauth2_provider/accesstoken/add/ The token can be anything, and the expiration date should just be today plus 10 years.

MITx Online Setup
-----------------

To set up MITx Online:


#. Get the gateway IP for the ``tutor_local_default`` network: ``docker network inspect tutor_local_default | grep Gateway``

   * Mac users should instead use the host.docker.internal IP. Specify this by using ``host-internal`` in ``OPENEDX_IP``.

#. Set up your ``/etc/hosts`` file to point ``mitxonline.odl.local`` to localhost.
#. Clone the repository somewhere.
#. Set up your ``.env`` file. These settings need particular attention:

   * ``OPENEDX_IP``\ : set to the gateway IP from the first step
   * ``OPENEDX_API_BASE_URL``\ : set to http://local.overhang.io
   * ``OPENEDX_SERVICE_WORKER_USERNAME``\ : set to ``mitx_online_serviceworker`` (unless you changed this)
   * ``OPENEDX_SERVICE_WORKER_API_TOKEN``\ : set to the token you generated

#. Build the app: ``docker compose build``
#. Run migrations and configure Wagtail::

      docker compose run --rm web ./manage.py migrate
      docker compose run --rm web ./manage.py configure_wagtail

#. Run the ``configure_instance`` command::

      docker compose run --rm web ./manage.py configure_instance linux --gateway <ip> --tutor

   where ``<ip>`` is the IP from the first step. (On macOS, specify ``macos`` instead of ``linux``. You can also skip ``--gateway``.) You will need to supply passwords for the MITx Online superuser and test learner accounts. Make a note of the client ID and secret that it will print out at the end.


Tutor Setup, Part Two
---------------------

Note that some of these steps require editing the main configuration files for the production instance (which is also used for a local deployment). Most of the settings that need to be adjusted to get integration working are overridden by the default Tutor configuration, so you can't update them by setting ``config.yml``. If you're using the development Tutor build, you'll likely need to edit ``development.py`` rather than ``production.py`` as necessary.

These steps will also disable the AuthN SSO MFE, so from here on you'll get normal edX authentication screens (if you're not being bounced to MITx Online).


#. Get the gateway IP of the ``mitxonline_default`` Docker network::

      docker network inspect mitxonline_default | grep Gateway

#. Log into to edX using your superuser account, and make sure your session stays open. Sessions are pretty long-lived so this just means not closing the browser that you started the session in. (Part of this process will involve mostly breaking authentication so it's important that you are able to get into the admin.)
#. Stop Tutor: ``tutor local stop``
#. Change into the configuration root for Tutor::

      cd "$(tutor config printroot)"

#. Create a ``env/build/openedx/requirements/private.txt`` with the required extensions::

      social-auth-mitxpro
      mitxpro-openedx-extensions

#. Edit the ``env/apps/openedx/config/lms.env.yml`` file and add::

      FEATURES:
        SKIP_EMAIL_VALIDATION: true

   to the ``FEATURES`` block (should be at the top).
#. Edit the ``env/apps/openedx/settings/lms/production.py`` and/or ``env/apps/openedx/settings/lms/development.py`` settings file. (The former is used by a local instance, where the latter is used by both dev and nightly instances.)

   * Add to the end of the file:

      * ``THIRD_PARTY_AUTH_BACKENDS = ['social_auth_mitxpro.backends.MITxProOAuth2']``
      * ``AUTHENTICATION_BACKENDS.append('social_auth_mitxpro.backends.MITxProOAuth2')``
      * ``IDA_LOGOUT_URI_LIST.append('http://mitxonline.odl.local:8013/logout/')`` - there's an existing one of these around like 300 in production.py too.

   * Find and update:

     * ``FEATURES['ENABLE_AUTHN_MICROFRONTEND'] = False`` (defaults to True)
     * ``REGISTRATION_EXTRA_FIELDS["terms_of_service"] = "hidden"`` (defaults to required)

#. Build a new ``openedx`` image: ``tutor images build openedx`` (this will take a long time)
#. Run a Docker Compse rebuild: ``tutor local dc build`` (this should be pretty quick - it's likely not required, just doing it here for safety)
#. Restart Tutor: ``tutor local start -d`` (omit ``-d`` if you want to watch the logs)
#. Check your settings. There's a ``print_setting`` command that you can use to verify everything is set properly:

   * ``tutor local run lms ./manage.py lms print_setting REGISTRATION_EXTRA_FIELDS``
   * ``tutor local run lms ./manage.py lms print_setting AUTHENTICATION_BACKENDS``
   * ``tutor local run lms ./manage.py lms print_setting FEATURES`` - will print a lot of stuff
   * ``tutor local run lms ./manage.py lms print_setting THIRD_PARTY_AUTH_BACKENDS``
   * If you do have weird errors or settings not showing properly, make sure you edited the right yaml files *and* that they're using the right whitespace (i.e. don't use tabs).

#. In a separate browser session of some kind (incognito/private browsing/other browser entirely), try to navigate to http://local.overhang.io . It should load but it should give you an error message. In the LMS logs, you should see an error message for "Can't fetch settings for disabled provider." This is proper operation - the OAuth2 settings aren't in place yet.
#. In the superuser session you have open, go to http://local.overhang.io/admin . This should work. If you've been logged out, you should still be able to get in. If you can't (for instance, if you're getting 500 errors), you will need to turn off ``ENABLE_THIRD_PARTY_AUTH`` in ``FEATURES``\ , restart Tutor using ``tutor local stop`` and ``start``\ , not using ``reboot``\ , then try again.
#. Go to http://local.overhang.io/admin/third_party_auth/oauth2providerconfig/add/ and add a provider configuration:

   * Enabled is checked.
   * Name: ``mitxonline``
   * Slug: ``mitxpro-oauth2``
   * Site: ``local.overhang.io``
   * Skip hinted login dialog is checked.
   * Skip registration form is checked.
   * Skip email verification is checked.
   * Sync learner profile data is checked.
   * Enable sso id verification is checked.
   * Backend name: ``mitxpro-oauth2``
   * Client ID and Client Secret: from record created by ``configure_instance`` when you set up MITx Online.
   * Other settings:

         {
            "AUTHORIZATION_URL": "\http://mitxonline.odl.local:8013/oauth2/authorize/",
            "ACCESS_TOKEN_URL": "\http://<MITXONLINE_GATEWAY_IP>:8013/oauth2/token/",
            "API_ROOT": "\http://<MITXONLINE_GATEWAY_IP>:8013/"
         }

     where MITXONLINE_GATEWAY_IP is the IP from the ``mitxonline_default`` network from the first step. **Mac users**, use ``host.docker.internal`` for MITXONLINE_GATEWAY_IP.

#. Configure Tutor for OAuth2 authentication from MITx Online.

   * Go to http://local.overhang.io/admin/oauth2_provider/application/ and either add or edit the ``edx-oauth-app`` entry.
   * Ensure these settings are set:

      * Name: ``edx-oauth-app``
      * Redirect uris: ``http://mitxonline.odl.local:8013/login/_private/complete``
      * Client type: ``Confidential``
      * Authorization grant type: ``Confidental``
      * Skip authorization is checked.

   * Save ``Client id`` and ``Client secret``.

#. Update your MITx Online ``.env`` file. Set ``OPENEDX_API_CLIENT_ID`` and ``OPENEDX_API_CLIENT_SECRET`` to the values from the record you created or updated in the last step.
#. You should now be able to run some MITx Online management commands to ensure the service worker is set up properly:

   * ``sync_courserun --all ALL`` should sync the two test courses (if you made them).
   * ``repair_missing_courseware_records`` should also work.

#. In the separate browser session from step 12, attempt to log in again. This time, you should be able to log in through MITx Online, and you should be able to get to the edX LMS dashboard. If not, then double-check your provider configuration settings and try again.

   * Unlike devstack, the Tutor instance has an Update button for the provider configuration, so you can just update the record you put in.
   * If you are still getting "Can't fetch settings" errors, *make sure* your Site is set properly - there are three options by default and only one works. (This was typically the problem I had.)

#. Optionally, log into the LMS Django Admin and make your MITx Online superuser account a superuser there too.

Other Notes
-----------

**Trying to set configuration settings via ``tutor config`` will undo the specialty configuration above.** If you need to make changes to the configuration, either manually edit the ``env/apps/openedx/config/lms.env.yml`` file or the ``env/apps/openedx/settings/lms/production.py`` file and restart your Tutor instance.

**Make sure your service worker account is active.** It's an easy checkbox to miss.

**Restarting** If you want to rebuild from scratch, make sure you ``docker image prune``. It's also recommended to remove the Tutor project root folder - ``tutor config printroot`` will tell you where that is.

**Running Multiple Tutor Instances** If you want to run more than one Tutor instance, it's pretty important to specify the project root explicitly or you may end up with one instance trying to use config files from another and things getting confused from there. `See the Tutor documentation for this. <https://docs.tutor.overhang.io/local.html#tutor-root>`_ (A suggestion: configure aliases to the ``tutor`` command that run ``tutor --root=<whatever>`` so you don't have to rely on environment variables, especially if you keep multiple terminal sessions going.)
