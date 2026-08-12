"""Shared HTTP client for communication with the CoopTrack Flask REST API."""

from __future__ import annotations

import os
from typing import Any

import requests


API_BASE_URL = os.getenv("COOPTRACK_API_URL", "http://api:4000").rstrip("/")
DEFAULT_TIMEOUT_SECONDS = 10


class ApiError(RuntimeError):
    """A user-safe description of an unsuccessful API request."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


def _request(
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None = None,
    json: dict[str, Any] | None = None,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> Any:
    """Send one API request and return its decoded JSON response."""
    url = f"{API_BASE_URL}/{path.lstrip('/')}"
    try:
        response = requests.request(
            method,
            url,
            params=params,
            json=json,
            timeout=timeout,
        )
    except requests.Timeout as error:
        raise ApiError("The CoopTrack API timed out. Please try again.") from error
    except requests.ConnectionError as error:
        raise ApiError(
            "The CoopTrack API is unavailable. Confirm that the API container is running."
        ) from error
    except requests.RequestException as error:
        raise ApiError(f"The API request could not be completed: {error}") from error

    try:
        payload = response.json()
    except ValueError as error:
        raise ApiError(
            "The CoopTrack API returned an invalid response.",
            status_code=response.status_code,
        ) from error

    if not response.ok:
        if isinstance(payload, dict):
            message = payload.get("error") or payload.get("message")
        else:
            message = None
        raise ApiError(
            message or f"The API returned HTTP {response.status_code}.",
            status_code=response.status_code,
        )

    return payload


def get(path: str, *, params: dict[str, Any] | None = None) -> Any:
    """Issue a GET request."""
    return _request("GET", path, params=params)


def post(path: str, payload: dict[str, Any]) -> Any:
    """Issue a POST request with a JSON body."""
    return _request("POST", path, json=payload)


def put(path: str, payload: dict[str, Any]) -> Any:
    """Issue a PUT request with a JSON body."""
    return _request("PUT", path, json=payload)


def delete(path: str) -> Any:
    """Issue a DELETE request."""
    return _request("DELETE", path)
