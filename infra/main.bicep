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

@description('Azure AI Foundry endpoint')
param azureAiEndpoint string = ''

@description('Existing Cosmos DB account name')
param existingCosmosDbName string = 'storycircuit-cosmosdb'

@description('Existing Cosmos DB resource group name')
param existingCosmosDbResourceGroup string = 'aiworkshop-rg'

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

// Reference existing Cosmos DB
resource existingCosmosDbRg 'Microsoft.Resources/resourceGroups@2021-04-01' existing = {
  scope: subscription()
  name: existingCosmosDbResourceGroup
}

resource existingCosmosDb 'Microsoft.DocumentDB/databaseAccounts@2023-04-15' existing = {
  scope: existingCosmosDbRg
  name: existingCosmosDbName
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
    cosmosEndpoint: existingCosmosDb.properties.documentEndpoint
    applicationInsightsConnectionString: monitoring.outputs.applicationInsightsConnectionString
    azureAiEndpoint: azureAiEndpoint
    azureTenantId: tenant().tenantId
  }
}

// Outputs
output AZURE_RESOURCE_GROUP_NAME string = rg.name
output AZURE_LOCATION string = location
output AZURE_CONTAINER_REGISTRY_NAME string = containerRegistry.outputs.name
output AZURE_CONTAINER_APPS_ENVIRONMENT_NAME string = containerAppsEnvironment.outputs.name
output AZURE_CONTAINER_APP_NAME string = containerApp.outputs.name
output AZURE_COSMOS_ENDPOINT string = existingCosmosDb.properties.documentEndpoint
output APPLICATION_INSIGHTS_CONNECTION_STRING string = monitoring.outputs.applicationInsightsConnectionString
output CONTAINER_APP_URL string = 'https://${containerApp.outputs.fqdn}'
