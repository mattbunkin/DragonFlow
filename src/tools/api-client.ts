/*
File that handles api requests to the flask server but automates
each api request to handle access token generation and mechanics
*/
import { get } from "svelte/store";
import {
  accessToken,
  refreshAccessToken,
  isTokenExpired,
} from "./token-service";

interface RequestOptions extends RequestInit {
  requiresAuth?: boolean;
}

// actual api client
export async function apiRequest<T = any>(
  endpoint: string,
  options: RequestOptions = {},
): Promise<T> {
  const requiresAuth = options.requiresAuth !== false;

  // define headers for pre the request
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  } as Record<string, string>;

  // where actual authorization for API begins
  if (requiresAuth) {
    const token = get(accessToken);

    // if access token is not valid
    if (!token) {
      // check if refresh token valid to make new access token
      const refreshed = await refreshAccessToken();
      if (!refreshed) {
        throw new Error("Authentication Required");
      }
    }
    // check if token is expired to get refresh token status
    else if (isTokenExpired(token)) {
      const refreshed = await refreshAccessToken();
      if (!refreshed) {
        throw new Error("Authentication Required");
      }
    }

    // get access token that is possibly refreshed and new
    const currentToken = get(accessToken);
    if (currentToken) {
      headers["Authorization"] = `Bearer ${currentToken}`;
    }
  }

  // finally after all auth: make API request
  try {
    const response = await fetch(`http://127.0.0.1:5000/${endpoint}`, {
      ...options,
      headers,
      credentials: "include",
    });

    if (response.status === 401 && requiresAuth) {
      // try and get refresh token status to see if we can validate token
      const refreshed = await refreshAccessToken();
      if (refreshed) {
        // retry request with brand new local access token
        const newToken = get(accessToken);
        headers["Authorization"] = `Bearer ${newToken}`;

        // newly attempted API request
        const retryResponse = await fetch(`http://127.0.0.1:5000/${endpoint}`, {
          ...options,
          headers,
          credentials: "include",
        });

        if (retryResponse.ok) {
          return await retryResponse.json();
        } else {
          throw new Error(`API request retry failed: ${retryResponse.status}`);
        }
      } else {
        throw new Error(
          `Authentication process failed: Couldn't access refresh token or access token..`,
        );
      }
    }

    if (!response.ok) {
      throw new Error(
        `API request failed for standard api request: ${response.status}`,
      );
    }

    return await response.json();
  } catch (error) {
    console.error("Complete endpoint access error", error);
    throw error;
  }
}
