#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

// Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[derive(Serialize, Deserialize, Debug)]
struct ConnectionParts {
    host: String,
    port: String,
    email: String,
    password: String,
}

#[derive(Serialize, Deserialize, Debug)]
struct JSONResponse {
    json: HashMap<String, String>,
}

async fn login(connection_parts: ConnectionParts) -> Result<reqwest::Response, reqwest::Error> {
    let client = reqwest::Client::new();
    let mut body = HashMap::new();

    body.insert("email", &connection_parts.email);
    body.insert("password", &connection_parts.password);

    let mut new_host = String::from("http://");
    let host: &str = if connection_parts.host.starts_with("http://") {
        new_host.push_str(&connection_parts.host.trim_start_matches("http://"));
        new_host.push_str(":");
        new_host.push_str(&connection_parts.port);

        &new_host
    } else {
        new_host.push_str(&connection_parts.host);
        new_host.push_str(":");
        new_host.push_str(&connection_parts.port);

        &new_host
    };

    let result = client
        .post(format!("{}/user/token/", &host))
        .json(&body)
        .send()
        .await;

    return result;
}

#[tauri::command]
async fn test_connection(connection_parts: ConnectionParts) -> Result<bool, bool> {
    let result = match login(connection_parts).await {
        Ok(res) => match res.status() {
            reqwest::StatusCode::OK => true,
            reqwest::StatusCode::CREATED => true,
            _ => {
                println!("{}", res.status());
                false
            }
        },
        Err(err) => {
            println!("An error occurred! {}", err);
            false
        }
    };

    return Ok(result);
}

#[derive(Deserialize)]
struct TokenResult {
    token: String,
}

#[tauri::command]
async fn connect(connection_parts: ConnectionParts) -> Result<String, bool> {
    let result = match login(connection_parts).await {
        Ok(res) => match res.status() {
            reqwest::StatusCode::OK => {
                let data = res.json::<TokenResult>().await.unwrap();
                println!("{}", data.token);
                data.token
            }
            _ => {
                println!("{}", res.status());
                String::from("")
            }
        },
        Err(err) => String::from(""),
    };

    return Ok(result);
}

#[tauri::command]
async fn open_graph_viewer(handle: tauri::AppHandle) {
    println!("Opening Graph Viewer...");
    let graph_viewer_window = tauri::WindowBuilder::new(&handle, "graph-viewer", tauri::WindowUrl::App("/graph-viewer".parse().unwrap()))
        .title("Graph Viewer")
        .resizable(true)
        .build()
        .unwrap();
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet, test_connection, connect, open_graph_viewer])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
