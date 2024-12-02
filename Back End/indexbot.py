from chatbot.chatbot_functions import send_email, fetch_emails, book_meeting, get_all_work_items, get_all_risk_items, get_all_users, get_total_priority_by_user
\
    
def run_tests():
    print("Running Tests...")
    
    # Test send_email
    print("\nTesting send_email...")
    result = send_email("Test Subject", "Test Body", ["test@example.com"], [])
    print("Result:", result)
    
    # Test fetch_emails
    print("\nTesting fetch_emails...")
    result = fetch_emails()
    print("Result:", result)
    
    # Test book_meeting
    print("\nTesting book_meeting...")
    result = book_meeting(
        "Meeting Subject", 
        "2024-12-02T10:00:00", 
        "2024-12-02T11:00:00", 
        ["test@example.com"]
    )
    print("Result:", result)
    
    # Test get_all_work_items
    print("\nTesting get_all_work_items...")
    result = get_all_work_items()
    print("Result:", result)
    
    # Test get_all_risk_items
    print("\nTesting get_all_risk_items...")
    result = get_all_risk_items()
    print("Result:", result)
    
    # Test get_all_users
    print("\nTesting get_all_users...")
    result = get_all_users()
    print("Result:", result)
    
    # Test get_total_priority_by_user
    print("\nTesting get_total_priority_by_user...")
    result = get_total_priority_by_user()
    print("Result:", result)

# Run the tests
run_tests()
