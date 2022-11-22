# Development

## Setup

- Install [rust](https://www.rust-lang.org/learn/get-started)
- Install [yarn](https://classic.yarnpkg.com/lang/en/docs/install/)
- Run `yarn install`
- Run `yarn setup:ui`

## Running the Dev Server

- To start the development server along with the tauri instance run `yarn tauri dev`. You will see an application window popup.

- To start only the NextJS development server run `yarn dev`. Then go to `localhost:1420` to view the website.

## Building the Application

- Run `yarn tauri build` to build the application.

- To build for linux you may need to install the following packages

```
sudo apt install libwebkit2gtk-4.0-dev \
    build-essential \
    curl \
    wget \
    libssl-dev \
    libgtk-3-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev \
    pkg-config \
    libssl-dev \
    libdbus-1-dev \
```

- To build for windows you'll need to install rust for windows and node.js for windows
  - Once you have node install you might have to run `corepack enable` to activate yarn