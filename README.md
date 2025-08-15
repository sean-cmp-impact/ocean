# GitGuardian

An integration used to import GitGuardian resources into Port.

## Configuration

This integration uses API keys for authentication. View the [GitGuardian documentation](https://docs.gitguardian.com/api-docs/authentication#creating-your-api-key) for guidance on how to create an API Key. 

You'll also need to configure the following environment variables as shown in the [.env.example](.env.example) file:

### Required Environment Variables

- `OCEAN__INTEGRATION__CONFIG__GITGUARDIAN_API_BASE_URL`: The GitGuardian [API base URL](https://api.gitguardian.com/docs#section/Introduction). 
- `OCEAN__INTEGRATION__CONFIG__GITGUARDIAN_API_VERSION`: The GitGuardian API version, e.g., **v1**
- `OCEAN__INTEGRATION__CONFIG__GITGUARDIAN_API_TOKEN`: Your [GitGuardian API Token](https://docs.gitguardian.com/api-docs/authentication#creating-your-api-key)
- `OCEAN__INTEGRATION__CONFIG__GITGUARDIAN_WEBHOOK_SECRET`: Your [GitGuardian Webhook Signature Token](https://docs.gitguardian.com/platform/configure-alerting/notifiers-integrations/custom-webhook#how-to-verify-the-payload-signature)
- `OCEAN__PORT__CLIENT_ID`: Your Port OAuth client ID
- `OCEAN__PORT__CLIENT_SECRET`: Your Port OAuth client secret
- `OCEAN__BASE_URL`: The base URL of your Ocean instance

## Resources

This integration provides the following resources:
- **source**: Sources that GitGuardian scans to detect secret incidents, e.g., `GitHub`, `Jira`, `Slack`, and `Confluence`
- **secret_detector**: GitGuardian secret detectors
- **internal_secret_incident**: Internal secret incidents found by GitGuardian
- **public_secret_incident**: Public secret incidents found by GitGuardian
- **user**: GitGuardian users, also known as workspace members

#### Install & use the integration - [Integration documentation](https://docs.port.io/build-your-software-catalog/sync-data-to-catalog/)

#### Develop & improve the integration - [Ocean integration development documentation](https://ocean.getport.io/develop-an-integration/)