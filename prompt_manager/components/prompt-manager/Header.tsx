import React from 'react'
import styles from './PromptManager.module.css'

export function Header({ searchQuery, setSearchQuery }) {
  return (
    <header className={styles.header}>
      <div className={styles.headerContent}>
        <input
          type="text"
          placeholder="Search prompts..."
          className={styles.searchInput}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button className={styles.newPromptButton}>
          New Prompt
        </button>
      </div>
    </header>
  )
}