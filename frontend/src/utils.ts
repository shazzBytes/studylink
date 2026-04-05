import { AxiosError } from "axios"
import type { ApiError } from "./client"

function extractErrorMessage(err: ApiError): string {
  if (err instanceof AxiosError) {
    return err.message
  }

  const errDetail = (err.body as any)?.detail
  if (Array.isArray(errDetail) && errDetail.length > 0) {
    return errDetail[0].msg
  }
  return errDetail || "Something went wrong."
}

export function handleError(err: ApiError, notifier?: (msg: string) => void) {
  const errorMessage = extractErrorMessage(err)
  const fn = notifier

  if (fn) {
    try {
      fn(errorMessage)
    } catch (err) {
      // If notifier throws, fall back to console
      // eslint-disable-next-line no-console
      console.error("Notifier failed:", err)
      // eslint-disable-next-line no-console
      console.error(errorMessage)
    }
  } else {
    // eslint-disable-next-line no-console
    console.error(errorMessage)
  }
}

export const createErrorHandler =
  (notifier: (msg: string) => void) =>
  (err: ApiError): void => {
    handleError(err, notifier)
  }

export const getInitials = (name: string): string => {
  return name
    .split(" ")
    .slice(0, 2)
    .map((word) => word[0])
    .join("")
    .toUpperCase()
}
