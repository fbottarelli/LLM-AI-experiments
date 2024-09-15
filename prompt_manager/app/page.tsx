import Link from "next/link"

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <h1>Welcome to Shadcn Components</h1>
      <div className="flex flex-col space-y-4">
        <Link href="/prompt-manager" className="text-blue-500 hover:underline">
          Go to Prompt Manager
        </Link>
        <Link href="/prompt-manager-alt" className="text-blue-500 hover:underline">
          Go to Alternative Prompt Manager
        </Link>
      </div>
    </main>
  )
}
