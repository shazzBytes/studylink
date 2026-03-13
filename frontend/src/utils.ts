import { AxiosError } from "axios"
import type { ApiError } from "./client"

function extractErrorMessage(err: unknown): string {
  if (err instanceof AxiosError) {
    return err.message
  }

  if (!(err && typeof err === "object")) {
    return "Something went wrong."
  }

  const errBody = (err as ApiError).body as { detail?: unknown } | undefined
  const errDetail = errBody?.detail
  if (Array.isArray(errDetail) && errDetail.length > 0) {
    return String((errDetail[0] as { msg?: string }).msg ?? "Something went wrong.")
  }
  return typeof errDetail === "string" ? errDetail : "Something went wrong."
}

export function handleError(
  this: ((msg: string) => void) | void,
  err: unknown,
  notifier?: unknown,
  ..._args: unknown[]
) {
  const errorMessage = extractErrorMessage(err)
  let fn: ((msg: string) => void) | undefined = undefined

  if (typeof notifier === "function") {
    fn = notifier as (msg: string) => void
  } else if (typeof this === "function") {
    fn = this
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
