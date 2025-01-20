# IIS Reverse Proxy and Windows Authentication for Streamlit

credits - https://gist.github.com/stanorama/
### Introduction

Setting up a reverse proxy on IIS (Internet Information Services) allows us to take advantage of windows authentication.

This means we can limit access to a streamlit app to a specific Active Directory group, Local group or list of Active Directory users.

(I haven't tested https support yet).

### IIS Setup

IIS must be installed with additional roles:
Under the windows server manager, navigate to and select the Websocket Protocol.
Web Server (IIS) → Web Server → Application Development → Websocket Protocol

![image](https://user-images.githubusercontent.com/51097996/224706100-92238387-0f14-4e81-a5eb-837b4004148a.png)


Under the windows server manager, navigate to and select Windows Authentication.
Web Server (IIS) → Web Server → Security → Windows Authentication

![image](https://user-images.githubusercontent.com/51097996/224706201-8e0ac674-7df1-49ec-96cd-cc6d3a0da604.png)


### IIS Configuration

Download and install ARR (Application Request Routing)

https://www.iis.net/downloads/microsoft/application-request-routing

Download and install URL Rewrite

https://www.iis.net/downloads/microsoft/url-rewrite

### Application Request Routing

Open IIS Manager, ARR is only available on the top level connection (it doesn;t show as a feature on individual sites).

Under actions - Select 'Server Proxy Settings'

![image](https://user-images.githubusercontent.com/51097996/224706282-5931f2cc-e5e0-4dd1-a7fe-e06871facee5.png)


Configure the Options:

* Enable Proxy: ON
* HTTP version: pass through
* Keep alive: ON
* Reverde rewrite host in response header: ON
* Preserve client IP in the following header: X-Forwarded-For
* Include TCP port from client IP: OFF

![image](https://user-images.githubusercontent.com/51097996/224706379-7f8a0887-03b7-41ee-83cb-2509e55d77a8.png)

### Create IIS site

Create a site for your streamlit app. (Sites - Add website...)
Site Name: MyStreamLitApp (set an appopriate name)
Physical Path: Set the path to where you have your python files (This is only used to save the web.config file).
Port: 8666 (or any value you wish but do NOT set the same value as the port used by streamlit).


![image](https://user-images.githubusercontent.com/51097996/224706441-8d0fcf52-3068-4709-a400-fe5ee1a1deb6.png)



### URL Rewrite (Site Level)

On your site (MyStreamLitApp) open URL rewrite and create a new inbound rule:

Name: ReverseProxy (Can be any name you choose)
Pattern: .*
Rewrite URL: [http://localhost:8502/{R:0](http://localhost:8502/%7BR:0)}
(This port should match the port that the streamlit app is running on)
Stop Processing of subsequent rules: ON

![image](https://user-images.githubusercontent.com/51097996/224706524-8fec267f-fb7c-4707-ab6a-3e4c1b7fc585.png)


### Firewall

In Windows firewall, create a rule to block domain and public access to the port that the streamlit app runs on (8502 in this example).

(You should still be able to access the streamlit app directly if you remote desktop to the server and use a local browser installed on the server).

This is to ensure that a user cannot bypass the IIS proxy and use the streamlit app directly on its tornado web server.

Ensure that the IIS site port (8666 in this example) is allowed.

### Windows Authentication

On your site (MyStreamLitApp) open 'Authentication' and set the following:

* Anonymous authentication: Disabled
* Windows Authentication: Enabled

![image](https://user-images.githubusercontent.com/51097996/224728082-76450913-dc1f-4d84-b572-becb16ebfd85.png)

### Windows Authentication Rules

On your site (MyStreamLitApp) open 'Authentication Rules'.

* Remove any default rules.
* Add a rule for each AD group, Local Group or AD user that will be permitted to access the streamlit app.

![image](https://user-images.githubusercontent.com/51097996/224706638-edd7d0c7-866e-4862-ac8d-008858200e9a.png)


### Checking web.config

The web.config file under c:\streamlit\MyStreamLitApp should look something like this:

```

<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <rewrite>
            <rules>
                <rule name="ReverseProxy" stopProcessing="true">
                    <match url=".*" />
                    <action type="Rewrite" url="http://localhost:8502/{R:0}" logRewrittenUrl="true" />
                </rule>
            </rules>

        </rewrite>
        <security>
            <authorization>
                <remove users="*" roles="" verbs="" />
                <add accessType="Allow" roles="MyADgroup" />
            </authorization>
        </security>
    </system.webServer>
</configuration>
```

### Enabling Detailed Errors

While testing the configuration it may be helpful to return detailed errors to the browser:
On the top level connection, goto 'Error Pages' and then 'Edit Deature Settings...' and select 'Detailed errors'
Remember to turn this off once you go live.

![image](https://user-images.githubusercontent.com/51097996/224706689-a511c725-9089-46f8-9519-8297791cfbe5.png)


### Testing

Point your client browser to [http://myserver:8502](http://myserver:8502./)
(replace myserver with your server name!)
This request should timeout as the firewall will be blocking this port.

Point your client browser to [http://myserver:8666](http://myserver:8502./)
If you are logged on as a user that has been granted access you should see the streamlit app.
If you are logged in as a user that has not been granted access you should receive a 401 response (HTTP Error 401.2 - Unauthorized)

You can print the headers in the streamlit app, to see that the Authorization header has been passed.
```
    from streamlit.web.server.websocket_headers import _get_websocket_headers

    headers = _get_websocket_headers()
    print(headers)
```

### Trial and Error

These steps are listed to show which settings were not necessary but may have been required with other web servers.
I initially experimented with the following server variables (copied from the nginx setup), however I found they are not required.

```
<serverVariables>
    <set name="HTTP_X_FORWARDED_HOST" value="{HTTP_HOST}" />
    <set name="HTTP_X_FORWARDED_SCHEMA" value="http" />
    <set name="HTTP_X_FORWARDED_PROTO" value="http" />
    <set name="HTTP_UPGRADE" value="websocket" />
    <set name="HTTP_CONNECTION" value="upgrade" />
</serverVariables>
```

Additionally the disabling of CORS and XSRF Protection do not matter with IIS.

```
[server]
enableCORS = false
enableXsrfProtection = false
```

### Other

Unfortunately it is not possible to pass on the user name to streamlit, so the security is limited to accessible or not, it would not be possible to do fine grained control of streamlit page elements.

```
<serverVariables>
    <set name="HTTP_LOGON_USER" value="{LOGON_USER}" />
</serverVariables>
```



