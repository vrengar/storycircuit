// Main Bicep file for StoryCircuit infrastructure

targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the environment (e.g., dev, staging, prod)')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

@description('Id of the user or app to assign application roles')
param principalId string = ''

// Resource group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: 'rg-${environmentName}'
  location: location
}

// Container Apps Environment
module containerAppsEnvironment 'core/container-apps-environment.bicep' = {
  name: 'container-apps-environment'
  scope: rg
  params: {
    name: 'cae-${environmentName}'
    location: location
    logAnalyticsWorkspaceName: monitoring.outputs.logAnalyticsWorkspaceName
  }
}

// Container Registry
module containerRegistry 'core/container-registry.bicep' = {
  name: 'container-registry'
  scope: rg
  params: {
    name: 'cr${replace(environmentName, '-', '')}'
    location: location
  }
}

// Cosmos DB
module cosmosDb 'core/cosmos-db.bicep' = {
  name: 'cosmos-db'
  scope: rg
  params: {
    name: 'cosmos-${environmentName}'
    location: location
    databaseName: 'storycircuit'
    containerName: 'content'
  }
}

// Monitoring (Log Analytics + Application Insights)
module monitoring 'core/monitoring.bicep' = {
  name: 'monitoring'
  scope: rg
  params: {
    logAnalyticsName: 'log-${environmentName}'
    applicationInsightsName: 'appi-${environmentName}'
    location: location
  }
}

// Container App
module containerApp 'core/container-app.bicep' = {
  name: 'container-app'
  scope: rg
  params: {
    name: 'ca-storycircuit-${environmentName}'
    location: location
    containerAppsEnvironmentId: containerAppsEnvironment.outputs.id
    containerRegistryName: containerRegistry.outputs.name
    cosmosEndpoint: cosmosDb.outputs.endpoint
    applicationInsightsConnectionString: monitoring.outputs.applicationInsightsConnectionString
    azureAiEndpoint: '' // To be provided
    azureTenantId: tenant().tenantId
  }
}

// Outputs
output AZURE_RESOURCE_GROUP_NAME string = rg.name
output AZURE_LOCATION string = location
output AZURE_CONTAINER_REGISTRY_NAME string = containerRegistry.outputs.name
output AZURE_CONTAINER_APPS_ENVIRONMENT_NAME string = containerAppsEnvironment.outputs.name
output AZURE_CONTAINER_APP_NAME string = containerApp.outputs.name
output AZURE_COSMOS_ENDPOINT string = cosmosDb.outputs.endpoint
output APPLICATION_INSIGHTS_CONNECTION_STRING string = monitoring.outputs.applicationInsightsConnectionString
output CONTAINER_APP_URL string = containerApp.outputs.url
