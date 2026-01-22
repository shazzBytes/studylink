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
  // Support two calling styles used across the codebase:
  // 1) handleError.bind(showErrorToast) -> binds `this` to notifier
  // 2) handleError(error, showErrorToast) -> notifier passed explicitly
  const boundThis = (this as unknown) as unknown
  let fn: ((msg: string) => void) | undefined = undefined

  if (typeof notifier === "function") {
    fn = notifier
  } else if (typeof (boundThis as any) === "function") {
    fn = (boundThis as any) as (msg: string) => void
  }

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

export const getInitials = (name: string): string => {
  return name
    .split(" ")
    .slice(0, 2)
    .map((word) => word[0])
    .join("")
    .toUpperCase()
}
