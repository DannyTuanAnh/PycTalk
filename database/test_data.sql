-- Insert sample users for testing
INSERT INTO users (username, password_hash, email) VALUES
('testuser1', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'test1@example.com'), -- password: hello
('testuser2', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'test2@example.com'), -- password: test  
('testuser3', '64e604787cbf194841e7b68d7cd28786c3b3b91f10bd7e9fd9a4d0b0f4c2b8b0', 'test3@example.com'); -- password: demo

-- Create group_members table if not exists
CREATE TABLE IF NOT EXISTS group_members (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    group_id INT NOT NULL,
    user_id INT NOT NULL,
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES group_chat(group_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_membership (group_id, user_id)
);
