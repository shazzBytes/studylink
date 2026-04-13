import { AxiosError } from "axios"
import type { ApiError } from "./client"

function extractErrorMessage(err: unknown): string {
  if (err instanceof AxiosError) {
    return err.message
  }

  const apiLikeError = err as Partial<ApiError> & { body?: { detail?: unknown } }
  const errDetail = apiLikeError.body?.detail
  if (Array.isArray(errDetail) && errDetail.length > 0) {
    return String((errDetail[0] as { msg?: string })?.msg || "Something went wrong.")
  }
  if (typeof errDetail === "string") {
    return errDetail
  }
  if (err instanceof Error) {
    return err.message
  }
  return "Something went wrong."
}

export function handleError(err: unknown, notifier?: (msg: string) => void) {
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
  (err: unknown): void => {
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
