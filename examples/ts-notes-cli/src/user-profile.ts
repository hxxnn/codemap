export function currentUser(): string {
  return process.env.USER ?? "anonymous";
}
