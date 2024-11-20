#!/usr/bin/node

const fs = require("node:fs/promises");

// Get the environment variables.
const appName = process.env.APP_NAME;
const serverHost = process.env.SERVER_HOST.toLowerCase();
const serverPort = process.env.SERVER_PORT.toLowerCase();

// Construct the server url.
const serverURL = `http://${serverHost}:${serverPort}/v1/`;

const environmentVariables = {
  "{{APP_NAME}}": appName,
  "{{SERVER_URL}}": serverURL,
};

/**
 * Generates the `swagger.yml` configuration
 * file to be used by the `Swagger UI` container.
 */
async function generateSwaggerYMLFile() {
  try {
    await fs
      .readFile("swagger.yml.template", { encoding: "utf-8" })
      .then(async (templateData) => {
        const regex = /{{([A-Z_]+)}}/g;
        const templateVariables = templateData.match(regex);
        let data = templateData;
        for (key of templateVariables) {
          data = data.replace(key, environmentVariables[key]);
        }
        await fs.writeFile("swagger.yml", data);
      });
  } catch (error) {
    console.error(error);
  }
}

generateSwaggerYMLFile();
