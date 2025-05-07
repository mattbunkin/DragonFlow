/* 
File to handle access token flow through out web-app while 
securing api requests and responses:
*/

import { goto } from "$app/navigation";
import { writable } from "svelte/store";
import { browser } from "$app/environment";

// Check if code is running in browser before accessing localStorage
const getInitialToken = () => {
  if (browser) {
    return localStorage.getItem("accessToken") || null;
  }
  return null;
};

// Initialize stores with browser check
export const accessToken = writable<string | null>(getInitialToken());
export const isAuthenticated = writable<boolean>(!!getInitialToken());

// parse and decode jwt token to get exact expiration time
function getTokenExpiration(token: string): number | null {
  if (!token) return null;

  try {
    if (browser) {
      // based off JWT structure
      const payload = token.split(".")[1];

      // base64 decode and parse payload
      const decodedPayload = JSON.parse(atob(payload));

      // return expiration time in milliseconds
      return decodedPayload.exp * 1000; // in milliseconds
    }
    return null;
  } catch (error) {
    console.error(`Couldn't parse token: ${error}`);
    return null;
  }
}

let refreshTimeout: number | null = null;

// performs operation to automate token refresh BEFORE it expires
export function setupTokenRefresh(token: string): void {
  // clear any timeout before refreshing
  if (refreshTimeout) {
    clearTimeout(refreshTimeout);
    refreshTimeout = null;
  }

  const expiration = getTokenExpiration(token);
  if (!expiration) return;

  // get current time and then time until access token expires
  const now = Date.now();
  const timeUntilRefresh = Math.max(0, expiration - now - 5 * 60 * 1000);

  // for debugging purposes
  console.log(
    `Token will refresh in ${Math.floor(timeUntilRefresh / 60000)} minutes`,
  );

  // set timeout to refresh token before it expires
  refreshTimeout = window.setTimeout(() => {
    refreshAccessToken();
  }, timeUntilRefresh);
}
// store token and set up refresh
export function setAccessToken(token: string): void {
  // skip if token is null or empty
  if (!token) {
    clearAccessToken();
    return;
  }

  // store token in memory and localStorage
  if (browser) {
    accessToken.set(token);
    localStorage.setItem("accessToken", token);
  }

  isAuthenticated.set(true);

  // set up auto refresh before token expires
  setupTokenRefresh(token);
}

export function clearAccessToken(): void {
  accessToken.set(null);
  isAuthenticated.set(false);

  if (browser) {
    localStorage.removeItem("accessToken");
    if (refreshTimeout) {
      clearTimeout(refreshTimeout);
      refreshTimeout = null;
    }
  }
}

// function that returns a promise that resolves to a boolean
export async function refreshAccessToken(): Promise<boolean> {
  try {
    const response = await fetch("http://127.0.0.1:5000/auth/refresh-token", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },

      // always include cookies for Flask
      credentials: "include",
    });
    if (!response.ok) {
      const errorText = await response.text();
      console.error("API Error Response:", errorText);
      throw new Error(
        `Couldn't get the Refresh Tokens based off HTTP error ${response.status}`,
      );
    }

    // if the flask endpoint worked
    const data = await response.json();
    setAccessToken(data.user_access_token || data.access_token);
    return true;
  } catch (error) {
    console.error(
      `Failed to generate access token or get refresh token API: ${error}`,
    );

    // on failure revoke access token and redirect to login
    clearAccessToken();

    // redirect to login page
    await goto("/login");
    return false;
  }
}

export function initAuthentication(): void {
  if (!browser) return; // Skip if not in browser environment

  const token = localStorage.getItem("accessToken");

  // if token was successfully retrieved
  if (token) {
    accessToken.set(token);
    isAuthenticated.set(true);
    setupTokenRefresh(token);
  }
}

// checking if token is expired
export function isTokenExpired(token: string): boolean {
  const expiration = getTokenExpiration(token);
  if (!expiration) return true;

  // if millisecond time of right now is greater than expiration date hasn't expired yet
  return Date.now() >= expiration;
}
