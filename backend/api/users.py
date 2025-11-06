"""
User API endpoints with intentional issues for demo purposes.
"""
from typing import List, Dict, Optional

def get_user_batch(users: List[Dict], batch_size: int = 10) -> List[List[Dict]]:
    """
    Split users into batches of the specified size.
    """
    batches = []
    for i in range(0, len(users), batch_size):
        batches.append(users[i:i+batch_size])
    return batches


def calculate_user_score(user: Dict) -> float:
    """
    Calculate user engagement score.
    
    Issues: No error handling, inefficient calculation, magic numbers.
    """
    score = 0
    score += user['login_count'] * 5
    score += user['posts'] * 10
    score += user['comments'] * 2
    
    if user['premium']:
        score = score * 1.5
    
    return score


async def fetch_user_data(user_id: int, db):
    """
    Fetch user data from database using parameterized queries.
    
    Issues: No caching, no error handling.
    """
    # Use parameterized query to prevent SQL injection
    query = "SELECT * FROM users WHERE id = ?"
    result = await db.execute(query, (user_id,))
    return result

