# TurboPrint-logger Changelog

## [v0.2.7](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.2.6...v0.2.7) (2026-04-13)

### fix

- **project:** :bug: fixed known bugs ([673c43b](https://github.com/Artem-Boker/TurboPrint-logger/commit/673c43b2152e9ea3e8f0bedb898cbd6fc11f8bea))
- **project:** :bug: fixed known bugs ([f093aa8](https://github.com/Artem-Boker/TurboPrint-logger/commit/f093aa84aab2e85d7048e36a81b4f1772ca69a00))
- **project:** :bug: fixed known bugs ([ae90bc1](https://github.com/Artem-Boker/TurboPrint-logger/commit/ae90bc10e82728374c5bd6b24e12f9e46c352712))

## [v0.2.6](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.2.5...v0.2.6) (2026-03-28)

### fix

- **project:** :bug: harden config/handlers, replace std errors with custom exceptions ([1829ebd](https://github.com/Artem-Boker/TurboPrint-logger/commit/1829ebd344fe0baf54655a7ea53615ddf32fc388))

### docs

- **changelog:** :memo: add conventional changelog for v0.2.6 ([a08d901](https://github.com/Artem-Boker/TurboPrint-logger/commit/a08d901f27431e5638d346839297de6479c129cb))

## [v0.2.5](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.2.4...v0.2.5) (2026-03-26)

### feat

- **processors:** :sparkles: added processor interface ([421b730](https://github.com/Artem-Boker/TurboPrint-logger/commit/421b7305f6f6bb1ebe06364f160303e4e47299c2))
- **processors:** :sparkles: added new processors classes ([b9910cf](https://github.com/Artem-Boker/TurboPrint-logger/commit/b9910cf2d277c41efc2841c284f2c703f768dcd7))

### fix

- **managers:** :bug: added lock in managers methods ([6213bd5](https://github.com/Artem-Boker/TurboPrint-logger/commit/6213bd51aee4d120331d13675bbc5b1735217845))

### docs

- **changelog:** :memo: add conventional changelog for v0.2.5 ([2ebf4ac](https://github.com/Artem-Boker/TurboPrint-logger/commit/2ebf4acd58c4b7ddb7244da9f64e514af7ed93d9))

## [v0.2.4](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.2.3...v0.2.4) (2026-03-25)

### fix

- **project:** :bug: fixed several bugs ([6923bbb](https://github.com/Artem-Boker/TurboPrint-logger/commit/6923bbb37bca0a2afe1258dd11dc7952145a5315))
- **project:** :bug: fixed several bugs ([aa932d5](https://github.com/Artem-Boker/TurboPrint-logger/commit/aa932d50307220439bd369f9c384bb5e003981f6))
- **handlers:** :bug: fixed compress files bugs ([8994bbd](https://github.com/Artem-Boker/TurboPrint-logger/commit/8994bbd3fce5fefe0ffe95fb6f602d85affe1032))

### refactor

- **project:** :art: added **all** static variable to all project files ([1418202](https://github.com/Artem-Boker/TurboPrint-logger/commit/14182028d01d4987acba90ffa6235d80e7a14fb4))

### feat

- **handlers:** :sparkles: added compress option with gzip module in RotatingFile handlers ([a5ce7c7](https://github.com/Artem-Boker/TurboPrint-logger/commit/a5ce7c7b0089f7cc00e394dc88e37ea7cb07e8f9))
- **formatters:** :sparkles: added support for orjson in JSONFormatter ([53e281c](https://github.com/Artem-Boker/TurboPrint-logger/commit/53e281c23c5393e9bd70d6577a145e8354702c07))

### docs

- **changelog:** :memo: add conventional changelog for v0.2.4 ([7fb7d37](https://github.com/Artem-Boker/TurboPrint-logger/commit/7fb7d371fb1d13c44a5c6541fc323a4d1a61b054))

## [v0.2.3](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.2.2...v0.2.3) (2026-03-21)

### feat

- **handlers:** :sparkles: added timed rotating file handler ([65a6839](https://github.com/Artem-Boker/TurboPrint-logger/commit/65a6839eda3ddce54c9b2f8ac3dda82d4a93ad44))

### docs

- **changelog:** :memo: add conventional changelog for v0.2.3 ([6fd0e07](https://github.com/Artem-Boker/TurboPrint-logger/commit/6fd0e077b4d8274bc53ee9bde6c436d59e984c08))

## [v0.2.2](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.2.1...v0.2.2) (2026-03-21)

### fix

- **handlers:** :bug: fixed buffer reset timer and atexit ([e2f5ce1](https://github.com/Artem-Boker/TurboPrint-logger/commit/e2f5ce19a84a562a836ac82fac7159fb914357f4))
- **logger:** :bug: fix logger propagate handling and added version in project init file ([7b8d3b5](https://github.com/Artem-Boker/TurboPrint-logger/commit/7b8d3b5fe5a9936643cb8aa7f78828a5bda2a743))
- **handlers:** :bug: fixed buffer timer ([cb89d51](https://github.com/Artem-Boker/TurboPrint-logger/commit/cb89d51e78377546e4d59e6b61fc2db802da3169))
- **plugins:** :bug: fixed register all plugins ([71b084f](https://github.com/Artem-Boker/TurboPrint-logger/commit/71b084f2d8fad3b8b61e2fe6d0ef6edc2a3db7d1))

### feat

- **managers:** :sparkles: added config manager with yaml, json config parsers ([eacb0c9](https://github.com/Artem-Boker/TurboPrint-logger/commit/eacb0c95265983cb082bf8e316b9047d5c23af5b))

### docs

- **changelog:** :memo: add conventional changelog for v0.2.2 ([8336a0c](https://github.com/Artem-Boker/TurboPrint-logger/commit/8336a0cf0fd6181c7f6b5a000510d845a0cf6d49))

## [v0.2.1](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.2.0...v0.2.1) (2026-03-21)

### refactor

- **handlers:** :sparkles: add separator arg in file handler and remove Path in \_open_file ([f138164](https://github.com/Artem-Boker/TurboPrint-logger/commit/f138164ce14ab7ece75e809968a5e4c1bf149fb0))
- **decorators:** :art: applying field filtering logic to utils ([5bb2fe9](https://github.com/Artem-Boker/TurboPrint-logger/commit/5bb2fe95dd3538cd0ddbc29180cc01620207baaa))

### feat

- **handlers:** :sparkles: add rotating file handler based on standard file handler ([c88a44a](https://github.com/Artem-Boker/TurboPrint-logger/commit/c88a44a326fa67e433c72566768baf2304f97759))
- **handlers:** :sparkles: added buffer reset timer and fixed handling errors ([693f324](https://github.com/Artem-Boker/TurboPrint-logger/commit/693f324b477e3d6bb4a9bb02527b03caa74a7432))

### fix

- **levels:** :bug: fix emoji in register new level ([b02ab9d](https://github.com/Artem-Boker/TurboPrint-logger/commit/b02ab9d869c52f81bd0918def13f81c0e025b309))
- **logger:** :bug: fix logger status with False in create new logger managers ([9742d8c](https://github.com/Artem-Boker/TurboPrint-logger/commit/9742d8c47f157e7b53219188680239843ee0ad24))
- **record:** :bug: fix date_time initialization ([c79e8e0](https://github.com/Artem-Boker/TurboPrint-logger/commit/c79e8e0b9188085cad103b4a29e4e9c9a57f365e))
- **formatters:** :bug: fix mask dict in security formatter ([69f8f52](https://github.com/Artem-Boker/TurboPrint-logger/commit/69f8f52531dcd3cedfbb0f6888bcbd0cdcd616cf))

### docs

- **changelog:** :memo: add conventional changelog for v0.2.1 ([e272eef](https://github.com/Artem-Boker/TurboPrint-logger/commit/e272eef184cb09ebc058e0de6112e2161cba712a))

## [v0.2.0](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.1.0...v0.2.0) (2026-03-21)

### feat

- **exceptions:** :sparkles: added custom exceptions from SourceCraft AI ([ee0447d](https://github.com/Artem-Boker/TurboPrint-logger/commit/ee0447db20f9eea1c8059f331e9d234b1af950e3))
- **formatters:** :sparkles: add support for msgspec in json formatter ([9f469ad](https://github.com/Artem-Boker/TurboPrint-logger/commit/9f469ade61c4daf7f78e533c147c39bc532812bd))

### fix

- **exceptions:** :sparkles: edit custom exceptions with SourceCraft AI ([b2355b5](https://github.com/Artem-Boker/TurboPrint-logger/commit/b2355b5cdb3e9a443911de1e823c4ac08c5872b8))
- **project:** :bug: fix errors in record processing and add context update in manager ([8d5bc86](https://github.com/Artem-Boker/TurboPrint-logger/commit/8d5bc8626ced20e6e7cf0d87a96db228286d1df5))
- **core:** :bug: fix get_container bug and init import ([25327a0](https://github.com/Artem-Boker/TurboPrint-logger/commit/25327a0fcafbcb5298c107c89dd9f4aafe22ee5c))

### refactor

- **exceptions:** :recycle: edit custom exceptions ([f5c425c](https://github.com/Artem-Boker/TurboPrint-logger/commit/f5c425c3c1ecde85116e37b555e7956315ac152a))

### chore

- **git:** :wrench: update gitignore file ([270e059](https://github.com/Artem-Boker/TurboPrint-logger/commit/270e059688c4613309caff8ac24e21fbdc86aad3))

### docs

- **changelog:** :memo: add conventional changelog for v0.2.0 ([ee758bc](https://github.com/Artem-Boker/TurboPrint-logger/commit/ee758bc61c630a3e2dfa2fd1bc62bd97ace40b59))
