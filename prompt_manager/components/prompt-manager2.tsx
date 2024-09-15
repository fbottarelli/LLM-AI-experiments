import * as React from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { cn } from "@/lib/utils"

export default function PromptManager() {
  const [searchQuery, setSearchQuery] = React.useState("")

  const categories = [
    "Starred",
    "All Prompts",
    "Most Used",
    "Recent",
    "AI",
    "Marketing",
    "Coding",
  ]

  const prompts = [
    { id: 1, content: "Write a blog post about the benefits of artificial intelligence in healthcare. Focus on recent advancements and potential future applications.", category: "Marketing", starred: true },
    { id: 2, content: "Generate Python code for a simple web scraper that can extract product information from an e-commerce website. Include error handling and data storage functionality.", category: "Coding", starred: false },
    { id: 3, content: "Create an AI model that can predict stock market trends based on historical data and current news sentiment. Outline the steps and potential machine learning algorithms to use.", category: "AI", starred: true },
    { id: 4, content: "Design a logo for a sustainable energy company. The logo should incorporate elements that represent renewable energy sources and environmental conservation.", category: "Marketing", starred: false },
    { id: 5, content: "Explain the concept of quantum computing in simple terms. Include its potential applications and how it differs from classical computing.", category: "AI", starred: false },
    { id: 6, content: "Optimize this SQL query for better performance: SELECT * FROM users JOIN orders ON users.id = orders.user_id WHERE orders.status = 'completed' AND users.country = 'USA' ORDER BY orders.created_at DESC;", category: "Coding", starred: true },
  ]

  const filteredPrompts = prompts.filter((prompt) =>
    prompt.content.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="flex h-screen bg-[#f0f0f0] font-sans">
      {/* Sidebar */}
      <div className="w-48 bg-[#f5f5f5] border-r border-[#e0e0e0]">
        <Tabs defaultValue="All Prompts" className="w-full" orientation="vertical">
          <TabsList className="bg-transparent h-auto flex-col items-start p-0">
            {categories.map((category) => (
              <TabsTrigger
                key={category}
                value={category}
                className={cn(
                  "w-full justify-start px-2 py-1 text-left text-sm",
                  "data-[state=active]:bg-[#007AFF] data-[state=active]:text-white",
                  "hover:bg-[#e0e0e0]",
                  category === "Starred" && "text-[#007AFF] font-semibold"
                )}
              >
                {category === "Starred" && (
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 inline mr-1" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                )}
                {category}
              </TabsTrigger>
            ))}
          </TabsList>

          {categories.map((category) => (
            <TabsContent key={category} value={category} className="mt-0 flex-1">
              {/* Main Content */}
              <div className="flex-1 flex flex-col">
                {/* Header */}
                <header className="bg-[#f5f5f5] border-b border-[#e0e0e0] p-4">
                  <div className="max-w-3xl mx-auto flex items-center">
                    <Input
                      type="text"
                      placeholder="Search prompts..."
                      className="flex-1"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                    />
                    <Button className="ml-2 bg-[#007AFF] text-white hover:bg-[#0056b3]">
                      New Prompt
                    </Button>
                  </div>
                </header>

                {/* Prompt Cards */}
                <ScrollArea className="flex-1 p-4">
                  <div className="max-w-3xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-4">
                    {filteredPrompts.map((prompt) => (
                      <Card key={prompt.id} className="bg-white shadow-md">
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                          <CardTitle className="text-sm font-medium">Prompt #{prompt.id}</CardTitle>
                          <Button variant="ghost" size="icon" className={prompt.starred ? "text-[#007AFF]" : "text-[#ccc]"}>
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                            </svg>
                          </Button>
                        </CardHeader>
                        <CardContent>
                          <p className="text-sm text-[#666] h-24 overflow-hidden">
                            {prompt.content}
                          </p>
                        </CardContent>
                        <CardFooter className="flex justify-between">
                          <span className="text-xs font-medium text-[#007AFF] bg-[#E6F2FF] px-2 py-1 rounded-full">
                            {prompt.category}
                          </span>
                          <div className="flex space-x-2">
                            <Button variant="ghost" size="icon" className="text-[#666] hover:text-[#333]">
                              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                                <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
                                <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z" />
                              </svg>
                            </Button>
                            <Button variant="ghost" size="icon" className="text-[#666] hover:text-[#333]">
                              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                                <path d="M6 10a2 2 0 11-4 0 2 2 0 014 0zM12 10a2 2 0 11-4 0 2 2 0 014 0zM16 12a2 2 0 100-4 2 2 0 000 4z" />
                              </svg>
                            </Button>
                          </div>
                        </CardFooter>
                      </Card>
                    ))}
                  </div>
                </ScrollArea>
              </div>
            </TabsContent>
          ))}
        </Tabs>
      </div>
    </div>
  )
}