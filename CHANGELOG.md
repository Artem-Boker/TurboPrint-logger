# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [v0.3.2](https://github.com/Artem-Boker/TurboPrint-logger/releases/tag/v0.3.2) - 2026-10-31

<small>[Compare with v0.3.1](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.3.1...v0.3.2)</small>

### Bug Fixes

- :bug: fixed known bugs ([764acc2](https://github.com/Artem-Boker/TurboPrint-logger/commit/764acc28ab4676d45ddf3a800a2227ffdafc0f7d) by Artem-Boker).

## [v0.3.1](https://github.com/Artem-Boker/TurboPrint-logger/releases/tag/v0.3.1) - 2026-04-19

<small>[Compare with v0.3.0](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.3.0...v0.3.1)</small>

### Features

- :sparkles: new processors and filters and add async to decorators and other ([a2769d0](https://github.com/Artem-Boker/TurboPrint-logger/commit/a2769d00189f42faf9fa22db8d9fa29cc61a0e99) by Artem-Boker).
- :sparkles: processors are divided into inner and outer ([3ed9cb9](https://github.com/Artem-Boker/TurboPrint-logger/commit/3ed9cb965bcbf8d80a04fdc71f17fcf159930fa7) by Artem-Boker).

### Bug Fixes

- :bug: fixed known bugs ([b1cfb90](https://github.com/Artem-Boker/TurboPrint-logger/commit/b1cfb902a11c37b98310027dbda20fd5d6df0853) by Artem-Boker).
- :recycle: updated levels ([97ae91e](https://github.com/Artem-Boker/TurboPrint-logger/commit/97ae91eee5086c89a7751225282c20bbde77760d) by Artem-Boker).

### Code Refactoring

- :recycle: rename LevelRegistry to LevelType ([e6fbc33](https://github.com/Artem-Boker/TurboPrint-logger/commit/e6fbc335c1b0dd1e9c0df6839ccbd3647ebd9e49) by Artem-Boker).

## [v0.3.0](https://github.com/Artem-Boker/TurboPrint-logger/releases/tag/v0.3.0) - 2026-04-17

<small>[Compare with v0.2.7](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.2.7...v0.3.0)</small>

### Bug Fixes

- :bug: fixed known bugs ([c39321c](https://github.com/Artem-Boker/TurboPrint-logger/commit/c39321cf4b3ba7a4e3927f05d65208e9ba4f4b5f) by Artem-Boker).

## [v0.2.7](https://github.com/Artem-Boker/TurboPrint-logger/releases/tag/v0.2.7) - 2026-04-13

<small>[Compare with v0.2.6](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.2.6...v0.2.7)</small>

### Bug Fixes

- :bug: fixed known bugs ([ae90bc1](https://github.com/Artem-Boker/TurboPrint-logger/commit/ae90bc10e82728374c5bd6b24e12f9e46c352712) by Artem-Boker).

## [v0.2.6](https://github.com/Artem-Boker/TurboPrint-logger/releases/tag/v0.2.6) - 2026-03-28

<small>[Compare with v0.2.5](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.2.5...v0.2.6)</small>

### Bug Fixes

- :bug: harden config/handlers, replace std errors with custom exceptions ([1829ebd](https://github.com/Artem-Boker/TurboPrint-logger/commit/1829ebd344fe0baf54655a7ea53615ddf32fc388) by Artem-Boker).

## [v0.2.5](https://github.com/Artem-Boker/TurboPrint-logger/releases/tag/v0.2.5) - 2026-03-26

<small>[Compare with v0.2.4](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.2.4...v0.2.5)</small>

### Features

- :sparkles: added new processors classes ([b9910cf](https://github.com/Artem-Boker/TurboPrint-logger/commit/b9910cf2d277c41efc2841c284f2c703f768dcd7) by Artem-Boker).
- :sparkles: added processor interface ([421b730](https://github.com/Artem-Boker/TurboPrint-logger/commit/421b7305f6f6bb1ebe06364f160303e4e47299c2) by Artem-Boker).

### Bug Fixes

- :bug: added lock in managers methods ([6213bd5](https://github.com/Artem-Boker/TurboPrint-logger/commit/6213bd51aee4d120331d13675bbc5b1735217845) by Artem-Boker).

### Performance Improvements

- :zap: replace manual copy to dataclass.replace ([7a97489](https://github.com/Artem-Boker/TurboPrint-logger/commit/7a974891c921b8ea15f37e57c884171043dc4e39) by Artem-Boker).

## [v0.2.4](https://github.com/Artem-Boker/TurboPrint-logger/releases/tag/v0.2.4) - 2026-03-25

<small>[Compare with v0.2.3](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.2.3...v0.2.4)</small>

### Features

- :sparkles: added support for orjson in JSONFormatter ([53e281c](https://github.com/Artem-Boker/TurboPrint-logger/commit/53e281c23c5393e9bd70d6577a145e8354702c07) by Artem-Boker).
- :sparkles: added compress option with gzip module in RotatinFile handlers ([a5ce7c7](https://github.com/Artem-Boker/TurboPrint-logger/commit/a5ce7c7b0089f7cc00e394dc88e37ea7cb07e8f9) by Artem-Boker).

### Bug Fixes

- :bug: fixed compress files bugs ([8994bbd](https://github.com/Artem-Boker/TurboPrint-logger/commit/8994bbd3fce5fefe0ffe95fb6f602d85affe1032) by Artem-Boker).
- :bug: fixed several bugs ([aa932d5](https://github.com/Artem-Boker/TurboPrint-logger/commit/aa932d50307220439bd369f9c384bb5e003981f6) by Artem-Boker).

### Code Refactoring

- :art: added __all__ static variable to all project files ([1418202](https://github.com/Artem-Boker/TurboPrint-logger/commit/14182028d01d4987acba90ffa6235d80e7a14fb4) by Artem-Boker).

## [v0.2.3](https://github.com/Artem-Boker/TurboPrint-logger/releases/tag/v0.2.3) - 2026-03-21

<small>[Compare with v0.2.2](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.2.2...v0.2.3)</small>

### Features

- :sparkles: added timed rotating file handler ([65a6839](https://github.com/Artem-Boker/TurboPrint-logger/commit/65a6839eda3ddce54c9b2f8ac3dda82d4a93ad44) by Artem-Boker).

## [v0.2.2](https://github.com/Artem-Boker/TurboPrint-logger/releases/tag/v0.2.2) - 2026-03-21

<small>[Compare with v0.2.1](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.2.1...v0.2.2)</small>

### Features

- :sparkles: added config manager with yaml, json config parsers ([eacb0c9](https://github.com/Artem-Boker/TurboPrint-logger/commit/eacb0c95265983cb082bf8e316b9047d5c23af5b) by Artem-Boker).

### Bug Fixes

- :bug: fixed register all plugins ([71b084f](https://github.com/Artem-Boker/TurboPrint-logger/commit/71b084f2d8fad3b8b61e2fe6d0ef6edc2a3db7d1) by Artem-Boker).
- :bug: fixed buffer timer ([cb89d51](https://github.com/Artem-Boker/TurboPrint-logger/commit/cb89d51e78377546e4d59e6b61fc2db802da3169) by Artem-Boker).
- :bug: fix logger propagate handling and added version in project init file ([7b8d3b5](https://github.com/Artem-Boker/TurboPrint-logger/commit/7b8d3b5fe5a9936643cb8aa7f78828a5bda2a743) by Artem-Boker).
- :bug: fixed buffer reset timer and atexit ([e2f5ce1](https://github.com/Artem-Boker/TurboPrint-logger/commit/e2f5ce19a84a562a836ac82fac7159fb914357f4) by Artem-Boker).

## [v0.2.1](https://github.com/Artem-Boker/TurboPrint-logger/releases/tag/v0.2.1) - 2026-03-21

<small>[Compare with v0.2.0](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.2.0...v0.2.1)</small>

### Features

- :sparkles: added buffer reset timer and fixed handling errors ([693f324](https://github.com/Artem-Boker/TurboPrint-logger/commit/693f324b477e3d6bb4a9bb02527b03caa74a7432) by Artem-Boker).
- :sparkles: add rotating file handler based on standard file handler ([c88a44a](https://github.com/Artem-Boker/TurboPrint-logger/commit/c88a44a326fa67e433c72566768baf2304f97759) by Artem-Boker).

### Bug Fixes

- :bug: fix mask dict in security formatter ([69f8f52](https://github.com/Artem-Boker/TurboPrint-logger/commit/69f8f52531dcd3cedfbb0f6888bcbd0cdcd616cf) by Artem-Boker).
- :bug: fix date_time initialization ([c79e8e0](https://github.com/Artem-Boker/TurboPrint-logger/commit/c79e8e0b9188085cad103b4a29e4e9c9a57f365e) by Artem-Boker).
- :bug: fix logger status with False in create new logger managers ([9742d8c](https://github.com/Artem-Boker/TurboPrint-logger/commit/9742d8c47f157e7b53219188680239843ee0ad24) by Artem-Boker).
- :bug: fix emoji in register new level ([b02ab9d](https://github.com/Artem-Boker/TurboPrint-logger/commit/b02ab9d869c52f81bd0918def13f81c0e025b309) by Artem-Boker).

### Performance Improvements

- :zap: moving patterns compilation outside of functions ([361db2f](https://github.com/Artem-Boker/TurboPrint-logger/commit/361db2f807d5bee61a29aca106c73b6f86d503cc) by Artem-Boker).

### Code Refactoring

- :art: applying field filtering logic to utils ([5bb2fe9](https://github.com/Artem-Boker/TurboPrint-logger/commit/5bb2fe95dd3538cd0ddbc29180cc01620207baaa) by Artem-Boker).
- :sparkles: add separator arg in file handler and remove Path in _open_file ([f138164](https://github.com/Artem-Boker/TurboPrint-logger/commit/f138164ce14ab7ece75e809968a5e4c1bf149fb0) by Artem-Boker).

## [v0.2.0](https://github.com/Artem-Boker/TurboPrint-logger/releases/tag/v0.2.0) - 2026-03-21

<small>[Compare with v0.1.0](https://github.com/Artem-Boker/TurboPrint-logger/compare/v0.1.0...v0.2.0)</small>

### Features

- :sparkles: add support for msgspec in json formatter ([9f469ad](https://github.com/Artem-Boker/TurboPrint-logger/commit/9f469ade61c4daf7f78e533c147c39bc532812bd) by Artem-Boker).
- :sparkles: added custom exceptions from SourceCraft AI ([ee0447d](https://github.com/Artem-Boker/TurboPrint-logger/commit/ee0447db20f9eea1c8059f331e9d234b1af950e3) by Artem-Boker).

### Bug Fixes

- :bug: fix get_container bug and init import ([25327a0](https://github.com/Artem-Boker/TurboPrint-logger/commit/25327a0fcafbcb5298c107c89dd9f4aafe22ee5c) by Artem-Boker).
- :bug: fix errors in record processing and add context update in manager ([8d5bc86](https://github.com/Artem-Boker/TurboPrint-logger/commit/8d5bc8626ced20e6e7cf0d87a96db228286d1df5) by Artem-Boker).
- :sparkles: edit custom exceptions with SourceCraft AI ([b2355b5](https://github.com/Artem-Boker/TurboPrint-logger/commit/b2355b5cdb3e9a443911de1e823c4ac08c5872b8) by Artem-Boker).

### Code Refactoring

- :recycle: edit custom exceptions ([f5c425c](https://github.com/Artem-Boker/TurboPrint-logger/commit/f5c425c3c1ecde85116e37b555e7956315ac152a) by Artem-Boker).

## [v0.1.0](https://github.com/Artem-Boker/TurboPrint-logger/releases/tag/v0.1.0) - 2026-03-18

<small>[Compare with first commit](https://github.com/Artem-Boker/TurboPrint-logger/compare/eee6f9facabdc352c2ea459f03f8634dde1566b6...v0.1.0)</small>

### Features

- :tada: initial commit ([eee6f9f](https://github.com/Artem-Boker/TurboPrint-logger/commit/eee6f9facabdc352c2ea459f03f8634dde1566b6) by Artem-Boker).

