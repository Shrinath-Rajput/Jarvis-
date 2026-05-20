/**
 * Authentication Service
 * Centralized auth logic for signup, login, logout, and user management
 */

const USERS_KEY = 'jarvis_users';
const CURRENT_USER_KEY = 'jarvis_current_user';

/**
 * Get all users from localStorage
 */
export const getAllUsers = () => {
  try {
    const users = localStorage.getItem(USERS_KEY);
    return users ? JSON.parse(users) : [];
  } catch (err) {
    console.error('Error getting users:', err);
    return [];
  }
};

/**
 * Save users to localStorage
 */
const saveUsers = (users) => {
  try {
    console.log('💾 Saving users to localStorage:', users.length, 'users');
    localStorage.setItem(USERS_KEY, JSON.stringify(users));
    return true;
  } catch (err) {
    console.error('Error saving users:', err);
    return false;
  }
};

/**
 * Signup - Create new account
 */
export const signup = (name, email, password) => {
  console.log('📝 SIGNUP ATTEMPT:', { name, email });

  // Trim and validate
  const trimmedName = name?.trim() || '';
  const trimmedEmail = email?.trim().toLowerCase() || '';
  const trimmedPassword = password?.trim() || '';

  // Validation
  if (!trimmedName || trimmedName.length < 2) {
    const error = 'Name must be at least 2 characters';
    console.error('❌ ' + error);
    return { success: false, error };
  }

  if (!trimmedEmail || !trimmedEmail.includes('@')) {
    const error = 'Please enter a valid email';
    console.error('❌ ' + error);
    return { success: false, error };
  }

  if (!trimmedPassword || trimmedPassword.length < 6) {
    const error = 'Password must be at least 6 characters';
    console.error('❌ ' + error);
    return { success: false, error };
  }

  // Check for duplicate email
  const users = getAllUsers();
  if (users.find(u => u.email === trimmedEmail)) {
    const error = 'Email already registered';
    console.error('❌ ' + error);
    return { success: false, error };
  }

  // Create new user
  const newUser = {
    id: Date.now().toString(),
    name: trimmedName,
    email: trimmedEmail,
    password: trimmedPassword,
    createdAt: new Date().toISOString(),
    lastActive: new Date().toISOString(),
  };

  // Add to users array (NEVER overwrite)
  users.push(newUser);
  if (!saveUsers(users)) {
    return { success: false, error: 'Failed to save user' };
  }

  console.log('✅ SIGNUP SUCCESS:', trimmedEmail);
  console.log('👥 Users:', users);

  // Return user data (without password)
  return {
    success: true,
    user: {
      id: newUser.id,
      name: newUser.name,
      email: newUser.email,
      createdAt: newUser.createdAt,
    },
  };
};

/**
 * Login - Authenticate user
 */
export const login = (email, password) => {
  console.log('🔐 LOGIN ATTEMPT:', { email });

  // Trim and validate
  const trimmedEmail = email?.trim().toLowerCase() || '';
  const trimmedPassword = password?.trim() || '';

  if (!trimmedEmail) {
    const error = 'Email is required';
    console.error('❌ ' + error);
    return { success: false, error };
  }

  if (!trimmedPassword) {
    const error = 'Password is required';
    console.error('❌ ' + error);
    return { success: false, error };
  }

  // Find user by email
  const users = getAllUsers();
  console.log('🔍 Searching for user:', trimmedEmail, 'in', users.length, 'users');
  
  const user = users.find(u => u.email === trimmedEmail);

  if (!user) {
    const error = 'User not found. Please sign up first.';
    console.error('❌ ' + error);
    return { success: false, error };
  }

  // Compare password (exact match after trimming)
  if (user.password !== trimmedPassword) {
    const error = 'Invalid password';
    console.error('❌ ' + error);
    console.log('   Expected:', user.password);
    console.log('   Got:', trimmedPassword);
    return { success: false, error };
  }

  // Update last active
  const updatedUsers = users.map(u =>
    u.email === trimmedEmail
      ? { ...u, lastActive: new Date().toISOString() }
      : u
  );
  saveUsers(updatedUsers);

  // Save current user to localStorage
  const currentUser = {
    id: user.id,
    name: user.name,
    email: user.email,
    loginTime: new Date().toISOString(),
  };

  try {
    localStorage.setItem(CURRENT_USER_KEY, JSON.stringify(currentUser));
    console.log('✅ LOGIN SUCCESS:', trimmedEmail);
    console.log('💾 Saved current user:', currentUser);
  } catch (err) {
    console.error('Error saving current user:', err);
  }

  return {
    success: true,
    user: currentUser,
  };
};

/**
 * Logout - Clear current user
 */
export const logout = () => {
  console.log('🚪 LOGOUT');
  try {
    localStorage.removeItem(CURRENT_USER_KEY);
    console.log('✅ LOGOUT SUCCESS - Cleared localStorage');
    return true;
  } catch (err) {
    console.error('Error during logout:', err);
    return false;
  }
};

/**
 * Get current logged-in user
 */
export const getCurrentUser = () => {
  try {
    const user = localStorage.getItem(CURRENT_USER_KEY);
    if (user) {
      const parsedUser = JSON.parse(user);
      console.log('👤 Current user:', parsedUser.email);
      return parsedUser;
    }
    console.log('👤 No current user');
    return null;
  } catch (err) {
    console.error('Error getting current user:', err);
    return null;
  }
};

/**
 * Check if user is authenticated
 */
export const isAuthenticated = () => {
  return getCurrentUser() !== null;
};

/**
 * Initialize auth (check for existing session on app load)
 */
export const initializeAuth = () => {
  console.log('🔄 Initializing authentication...');
  const user = getCurrentUser();
  if (user) {
    console.log('✅ Auto-login: Found existing session for', user.email);
    return user;
  }
  console.log('ℹ️ No existing session');
  return null;
};

export default {
  signup,
  login,
  logout,
  getCurrentUser,
  isAuthenticated,
  initializeAuth,
  getAllUsers,
};
