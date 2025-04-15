@description('Name of Azure App Configuration store')
param configStoreName string

@description('The principal ID of the application that needs read access to the Azure App Configuration store')
param appPrincipalId string

@description('The principal ID of the service principal that needs to manage the Azure App Configuration store')
param userPrincipalId string

resource configStore 'Microsoft.AppConfiguration/configurationStores@2023-03-01' existing = {
  name: configStoreName
}

var configStoreDataReaderRole = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '516239f1-63e1-4d78-a4de-a74fb236a071')
var configStoreDataOwnerRole = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '5ae67dd6-50cb-40e7-96ff-dc2bfa4b606b')

resource configStoreDataReaderRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().id, resourceGroup().id, appPrincipalId, configStoreDataReaderRole)
  scope: configStore
  properties: {
    roleDefinitionId: configStoreDataReaderRole
    principalId: appPrincipalId
  }
}

resource configStoreDataOwnerRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, userPrincipalId, configStoreDataOwnerRole)
  scope: configStore
  properties: {
    roleDefinitionId: configStoreDataOwnerRole
    principalId: userPrincipalId
  }
}
