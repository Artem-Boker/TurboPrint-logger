# TurboPrint-logger Changelog

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

- **changelog:** :memo: add conventional changelog for v0.2.1 ([9f94c97](https://github.com/Artem-Boker/TurboPrint-logger/commit/9f94c9721e7ab2178b8560705fea2452fc1f60b3))

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
