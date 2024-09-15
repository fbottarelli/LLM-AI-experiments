import { useState, useEffect } from 'react'
import axios from 'axios'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Search, Plus, Clipboard, Home, ChevronDown, Copy, MoreHorizontal, Star } from 'lucide-react'

interface Prompt {
  id: number;
  content: string;
  category: string;
}

export default function PromptManager() {
  const [activeCategory, setActiveCategory] = useState('All Prompts')
  const [searchQuery, setSearchQuery] = useState('')
  const [prompts, setPrompts] = useState<Prompt[]>([])

  const categories = [
    'All Prompts', 'Most Used', 'Recent', 'Starred', 'AI', 'Marketing', 'Coding'
  ]

  useEffect(() => {
    fetchPrompts()
  }, [])

  const fetchPrompts = async () => {
    try {
      const response = await axios.get<Prompt[]>('http://localhost:5000/api/prompts')
      setPrompts(response.data)
    } catch (error) {
      console.error('Error fetching prompts:', error)
    }
  }

  const createPrompt = async (content: string, category: string) => {
    try {
      const response = await axios.post<Prompt>('http://localhost:5000/api/prompts', { content, category })
      setPrompts([...prompts, response.data])
    } catch (error) {
      console.error('Error creating prompt:', error)
    }
  }

  const updatePrompt = async (id: number, content: string, category: string) => {
    try {
      await axios.put(`http://localhost:5000/api/prompts/${id}`, { content, category })
      setPrompts(prompts.map(prompt => prompt.id === id ? { ...prompt, content, category } : prompt))
    } catch (error) {
      console.error('Error updating prompt:', error)
    }
  }

  const deletePrompt = async (id: number) => {
    try {
      await axios.delete(`http://localhost:5000/api/prompts/${id}`)
      setPrompts(prompts.filter(prompt => prompt.id !== id))
    } catch (error) {
      console.error('Error deleting prompt:', error)
    }
  }

  const filteredPrompts = prompts.filter(prompt => 
    (activeCategory === 'All Prompts' || prompt.category === activeCategory) &&
    prompt.content.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="flex h-screen bg-[#f5f5f7]">
      {/* Sidebar */}
      <div className="w-64 bg-[#f0f0f2] border-r border-[#d1d1d6]">
        <div className="p-4">
          <h2 className="text-xl font-semibold mb-4 text-[#1d1d1f]">Categories</h2>
          <ScrollArea className="h-[calc(100vh-8rem)]">
            {categories.map((category) => (
              <Button
                key={category}
                variant={activeCategory === category ? "secondary" : "ghost"}
                className={`w-full justify-start mb-1 ${activeCategory === category ? 'bg-[#007aff] text-white' : 'text-[#1d1d1f] hover:bg-[#e5e5ea]'}`}
                onClick={() => setActiveCategory(category)}
              >
                {category}
              </Button>
            ))}
          </ScrollArea>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-[#ffffff] shadow-sm border-b border-[#d1d1d6]">
          <div className="max-w-7xl mx-auto py-2 px-4 sm:px-6 lg:px-8 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Button variant="ghost" className="text-[#007aff]">
                <Home className="h-5 w-5" />
              </Button>
              <Button variant="ghost" className="text-[#007aff]">
                Categories <ChevronDown className="ml-1 h-4 w-4" />
              </Button>
            </div>
            <div className="flex-1 max-w-lg mx-4">
              <div className="relative">
                <Search className="absolute left-2 top-2.5 h-4 w-4 text-[#86868b]" />
                <Input
                  type="search"
                  placeholder="Search prompts..."
                  className="pl-8 bg-[#f5f5f7] border-[#d1d1d6] focus:border-[#007aff] focus:ring-[#007aff]"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Button variant="ghost" className="text-[#007aff]">
                <Plus className="h-5 w-5" />
                <span className="ml-2">New Prompt</span>
              </Button>
              <Button variant="ghost" className="text-[#007aff]">
                <Clipboard className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </header>

        {/* Prompt Cards */}
        <main className="flex-1 overflow-y-auto p-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredPrompts.map((prompt) => (
              <Card key={prompt.id} className="bg-white border-[#d1d1d6] shadow-sm hover:shadow-md transition-shadow">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium text-[#1d1d1f]">
                    Prompt #{prompt.id}
                  </CardTitle>
                  <Button variant="ghost" size="icon" className="text-[#007aff]">
                    <Star className="h-4 w-4" />
                  </Button>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-[#86868b]">
                    {prompt.content.substring(0, 100)}...
                  </p>
                </CardContent>
                <CardFooter className="flex justify-between">
                  <Button variant="secondary" size="sm" className="bg-[#e5e5ea] text-[#1d1d1f] hover:bg-[#d1d1d6]">
                    {prompt.category}
                  </Button>
                  <div className="flex space-x-1">
                    <Button variant="ghost" size="icon" className="text-[#007aff]">
                      <Copy className="h-4 w-4" />
                    </Button>
                    <Button variant="ghost" size="icon" className="text-[#007aff]">
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </div>
                </CardFooter>
              </Card>
            ))}
          </div>
        </main>
      </div>
    </div>
  )
}