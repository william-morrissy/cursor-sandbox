"""
User API endpoints with intentional issues for demo purposes.
"""
from typing import List, Dict, Optional

def get_user_batch(users: List[Dict], batch_size: int = 10) -> List[List[Dict]]:
    """
    Split users into batches.
    
    Bug: Off-by-one error in slicing causes overlap between batches.
    """
    batches = []
    for i in range(0, len(users), batch_size):
        # BUG: This includes an extra item, causing overlap
        batches.append(users[i:i+batch_size+1])
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
    Fetch user data from database.
    
    Issues: No caching, SQL injection vulnerability, no error handling.
    """
    # Security issue: vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = await db.execute(query)
    return result

