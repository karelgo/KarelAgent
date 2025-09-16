output "resource_group_name" {
  description = "Name of the created resource group"
  value       = azurerm_resource_group.main.name
}

output "web_app_name" {
  description = "Name of the Azure Web App"
  value       = azurerm_linux_web_app.main.name
}

output "web_app_url" {
  description = "URL of the Azure Web App"
  value       = "https://${azurerm_linux_web_app.main.default_hostname}"
}

output "web_app_id" {
  description = "ID of the Azure Web App"
  value       = azurerm_linux_web_app.main.id
}

output "staging_slot_url" {
  description = "URL of the staging slot (if enabled)"
  value       = var.enable_staging_slot ? "https://${azurerm_linux_web_app_slot.staging[0].default_hostname}" : null
}

output "app_service_plan_id" {
  description = "ID of the App Service Plan"
  value       = azurerm_service_plan.main.id
}

output "application_insights_connection_string" {
  description = "Application Insights connection string"
  value       = azurerm_application_insights.main.connection_string
  sensitive   = true
}

output "application_insights_instrumentation_key" {
  description = "Application Insights instrumentation key"
  value       = azurerm_application_insights.main.instrumentation_key
  sensitive   = true
}

output "publish_profile" {
  description = "Publish profile for the web app (for use with GitHub Actions)"
  value       = azurerm_linux_web_app.main.site_credential[0].name
  sensitive   = true
}