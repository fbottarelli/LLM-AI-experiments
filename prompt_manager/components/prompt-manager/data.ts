export const categories = [
  'Starred', 'All Prompts', 'Most Used', 'Recent', 'AI', 'Marketing', 'Coding'
]

export const prompts = [
  { id: 1, content: 'Write a blog post about the benefits of artificial intelligence in healthcare. Focus on recent advancements and potential future applications.', category: 'Marketing', starred: true },
  { id: 2, content: 'Generate Python code for a simple web scraper that can extract product information from an e-commerce website. Include error handling and data storage functionality.', category: 'Coding', starred: false },
  { id: 3, content: 'Create an AI model that can predict stock market trends based on historical data and current news sentiment. Outline the steps and potential machine learning algorithms to use.', category: 'AI', starred: true },
  { id: 4, content: 'Design a logo for a sustainable energy company. The logo should incorporate elements that represent renewable energy sources and environmental conservation.', category: 'Marketing', starred: false },
  { id: 5, content: 'Explain the concept of quantum computing in simple terms. Include its potential applications and how it differs from classical computing.', category: 'AI', starred: false },
  { id: 6, content: 'Optimize this SQL query for better performance: SELECT * FROM users JOIN orders ON users.id = orders.user_id WHERE orders.status = "completed" AND users.country = "USA" ORDER BY orders.created_at DESC;', category: 'Coding', starred: true },
]