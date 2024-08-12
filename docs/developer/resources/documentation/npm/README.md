# NPM

## Description

NPM (Node Package Manager) is is a package manager for the JavaScript programming language. NPM includes a CLI that can be used to download and install software, known as packages. All npm packages are defined in files called package.json. `package.json` maintains the details, dependencies and state of your project.

## Documentation:

For more details on npm, please refer to the [official documentation](https://docs.npmjs.com/).

## package.json

-   `name`: If you plan to publish your package, the most important things in your package.json are the name and version fields as they will be required. The name and version together form an identifier that is assumed to be completely unique. Changes to the package should come along with changes to the version. If you don't plan to publish your package, the name and version fields are optional. The name is what your thing is called.
-   `description`: Put a description in it. It's a string. This helps people discover your package, as it's listed in `npm search`.
-   `version`: If you plan to publish your package, the most important things in your package.json are the name and version fields as they will be required. The name and version together form an identifier that is assumed to be completely unique. Changes to the package should come along with changes to the version. If you don't plan to publish your package, the name and version fields are optional.
-   `scripts`: The "scripts" property is a dictionary containing script commands that are run at various times in the lifecycle of your package. The key is the lifecycle event, and the value is the command to run at that point.
-   `dependencies`: Dependencies are specified in a simple object that maps a package name to a version range.
-   `devDependencies`: External packages, tests, or documentation framework not needed to build your project in production.
-   `peerDependencies`: In some cases, you want to express the compatibility of your package with a host tool or library, while not necessarily doing a `require` of this host. This is usually referred to as a plugin. Notably, your module may be exposing a specific interface, expected and specified by the host documentation.

## Commands

Here are some helpful commands:

-   `npm init`: Create a package.json file.
-   `npm install [<package@version>]`: Install a package.
-   `npm update [<package>]`: Update packages.
-   `npm ci`: Clean install a project.
-   `npm uninstall [<package>]`: Remove a package.
-   `npm ls`: List installed packages.
-   `npm docs [<package> [<package> ...]]`: Open documentation for a package in a web browser.
-   `npm help <term> [<terms...>]`: Get help on npm.
-   `npm run-script <command> [-- <args>]`: Run arbitrary package scripts.
-   `npx -- <package>[@<version>] [args...]`: Run a command from a local or remote npm package.

You may find more details and helpful commands [here](https://docs.npmjs.com/cli/v10/commands).
