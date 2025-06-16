-- Insert test user
INSERT INTO users (id, username, email, password, first_name, last_name, gender, phone)
VALUES (
  '1',
  'testuser',
  'test@example.com',
  '$2b$10$6jM7G6HXcBWqxA3DqcXYu.sFn5VXWJ0.U9HgI0RqgFRDDWVyV.Hy2', -- password: 'password123'
  'Test',
  'User',
  'Male',
  '1234567890'
); 