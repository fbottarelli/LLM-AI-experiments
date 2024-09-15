'use client'

import React, { useState } from 'react'
import { Sidebar } from './prompt-manager/Sidebar'
import { Header } from './prompt-manager/Header'
import { PromptCard } from './prompt-manager/PromptCard'
import { prompts, categories } from './prompt-manager/data'
import styles from './prompt-manager/PromptManager.module.css'

export function PromptManagerComponent() {
  const [activeCategory, setActiveCategory] = useState('All Prompts')
  const [searchQuery, setSearchQuery] = useState('')

  const filteredPrompts = prompts.filter(prompt => 
    (activeCategory === 'All Prompts' || 
     (activeCategory === 'Starred' && prompt.starred) ||
     prompt.category === activeCategory) &&
    prompt.content.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className={styles.container}>
      <Sidebar
        categories={categories}
        activeCategory={activeCategory}
        setActiveCategory={setActiveCategory}
      />
      <div className={styles.mainContent}>
        <Header
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
        />
        <main className={styles.promptGrid}>
          {filteredPrompts.map((prompt) => (
            <PromptCard key={prompt.id} prompt={prompt} />
          ))}
        </main>
      </div>
    </div>
  )
}