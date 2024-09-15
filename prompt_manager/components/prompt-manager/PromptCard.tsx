import React from 'react'
import styles from './PromptManager.module.css'

export function PromptCard({ prompt }) {
  return (
    <div className={styles.promptCard}>
      <div className={styles.promptCardHeader}>
        <h3 className={styles.promptTitle}>Prompt #{prompt.id}</h3>
        <button className={`${styles.starButton} ${prompt.starred ? styles.starred : ''}`}>
          <svg xmlns="http://www.w3.org/2000/svg" className={styles.starIcon} viewBox="0 0 20 20" fill="currentColor">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        </button>
      </div>
      <p className={styles.promptContent}>{prompt.content}</p>
      <div className={styles.promptCardFooter}>
        <span className={styles.promptCategory}>{prompt.category}</span>
        <div className={styles.promptActions}>
          <button className={styles.actionButton}>
            <svg xmlns="http://www.w3.org/2000/svg" className={styles.actionIcon} viewBox="0 0 20 20" fill="currentColor">
              <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
              <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z" />
            </svg>
          </button>
          <button className={styles.actionButton}>
            <svg xmlns="http://www.w3.org/2000/svg" className={styles.actionIcon} viewBox="0 0 20 20" fill="currentColor">
              <path d="M6 10a2 2 0 11-4 0 2 2 0 014 0zM12 10a2 2 0 11-4 0 2 2 0 014 0zM16 12a2 2 0 100-4 2 2 0 000 4z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  )
}