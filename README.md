# UniProm
UniProm is a custom tool for exporting specific data points from a Unifi controller to Prometheus. It was specifically made to support logging of lighting networks for the use in concert/festival/touring applications.

## Supported Data Points
* Snake status: Gets the status of an ethernet or fiber snake and whether or not the primary and backup connections are flipped

## Environment Variables
| Variable | Description |
| --- | --- |
| UNIFI_IP | IP or Hostname of Unifi controller | 
| UNIFI_USERNAME | Username for Unifi controller |
| UNIFI_PASSWORD | Password for Unifi controller |
| WEB_IP  | **(optional)** IP address of interface for Prometheus exporter |
| WEB_PORT | **(optional)** Port to host Prometheus exporter. Default=9430 |

## Deployment
UniProm is intended to be deployed using Docker. A Dockerfile is provided for building. Build the image using `docker build .`. 

## Development Environment
Uniprom uses environment variables to configure certain settings. During development, the .env file can be used to temporarily set environment variables. By default, this file is included in the .gitignore file, but an example file (.env.example) is available. Simply rename this file to .env and change the variables.