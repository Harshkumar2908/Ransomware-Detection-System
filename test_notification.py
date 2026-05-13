from plyer import notification

notification.notify(
    title="Test Notification",
    message="Notification Working!",
    timeout=10
)

print("Notification Sent")