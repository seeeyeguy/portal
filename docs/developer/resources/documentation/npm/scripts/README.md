# NPM Scripts

NPM Scripts are a set of built-in and custom scripts defined in the `package.json` file. Their goal is to provide a simple way to execute repetitive tasks, such as

-   Running a linter tool on your code
-   Executing the tests
-   Starting your project locally
-   Building your project
-   Minify or Uglify JS or CSS

We can run our scripts with the `npm run <script>` command.

Here are some predefined scripts included with this infrastructure.

1. `npm run dev`: Run a development site.
2. `npm run build`: Build site for production.
3. `npm run test`: Execute tests, exposing test coverage.
4. `lint`: Lint project with [`eslint`](https://eslint.org/).

You may find more information about npm scripts [here](https://docs.npmjs.com/cli/v6/using-npm/scripts).
