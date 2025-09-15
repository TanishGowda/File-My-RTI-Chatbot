// Supabase client configuration
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.REACT_APP_SUPABASE_URL || 'your_supabase_url_here'
const supabaseAnonKey = process.env.REACT_APP_SUPABASE_ANON_KEY || 'your_supabase_anon_key_here'

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  }
})

// Auth helper functions
export const auth = {
  // Sign up with email and password
  async signUp(email, password, fullName = null) {
    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: fullName
          }
        }
      })
      
      if (error) throw error
      return { data, error: null }
    } catch (error) {
      console.error('Sign up error:', error)
      return { data: null, error }
    }
  },

  // Sign in with email and password
  async signIn(email, password) {
    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password
      })
      
      if (error) throw error
      return { data, error: null }
    } catch (error) {
      console.error('Sign in error:', error)
      return { data: null, error }
    }
  },

  // Sign in with Google
  async signInWithGoogle() {
    try {
      const { data, error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${window.location.origin}/chat`
        }
      })
      
      if (error) throw error
      return { data, error: null }
    } catch (error) {
      console.error('Google sign in error:', error)
      return { data: null, error }
    }
  },

  // Sign out
  async signOut() {
    try {
      const { error } = await supabase.auth.signOut()
      if (error) throw error
      return { error: null }
    } catch (error) {
      console.error('Sign out error:', error)
      return { error }
    }
  },

  // Get current user
  getCurrentUser() {
    return supabase.auth.getUser()
  },

  // Listen to auth state changes
  onAuthStateChange(callback) {
    return supabase.auth.onAuthStateChange(callback)
  }
}

// Database helper functions
export const db = {
  // Get user profile
  async getProfile(userId) {
    try {
      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', userId)
        .single()
      
      if (error) throw error
      return { data, error: null }
    } catch (error) {
      console.error('Get profile error:', error)
      return { data: null, error }
    }
  },

  // Create user profile
  async createProfile(userId, email, fullName = null) {
    try {
      const { data, error } = await supabase
        .from('profiles')
        .insert({
          id: userId,
          email,
          full_name: fullName
        })
        .select()
        .single()
      
      if (error) throw error
      return { data, error: null }
    } catch (error) {
      console.error('Create profile error:', error)
      return { data: null, error }
    }
  },

  // Update user profile
  async updateProfile(userId, updates) {
    try {
      const { data, error } = await supabase
        .from('profiles')
        .update(updates)
        .eq('id', userId)
        .select()
        .single()
      
      if (error) throw error
      return { data, error: null }
    } catch (error) {
      console.error('Update profile error:', error)
      return { data: null, error }
    }
  },

  // Get user conversations
  async getConversations(userId) {
    try {
      const { data, error } = await supabase
        .rpc('get_user_conversations', { user_uuid: userId })
      
      if (error) throw error
      return { data, error: null }
    } catch (error) {
      console.error('Get conversations error:', error)
      return { data: null, error }
    }
  },

  // Create conversation
  async createConversation(userId, title) {
    try {
      const { data, error } = await supabase
        .from('conversations')
        .insert({
          user_id: userId,
          title
        })
        .select()
        .single()
      
      if (error) throw error
      return { data, error: null }
    } catch (error) {
      console.error('Create conversation error:', error)
      return { data: null, error }
    }
  },

  // Get conversation messages
  async getMessages(conversationId, userId) {
    try {
      const { data, error } = await supabase
        .rpc('get_conversation_messages', {
          conv_id: conversationId,
          user_uuid: userId
        })
      
      if (error) throw error
      return { data, error: null }
    } catch (error) {
      console.error('Get messages error:', error)
      return { data: null, error }
    }
  },

  // Add message
  async addMessage(conversationId, sender, content, metadata = {}) {
    try {
      const { data, error } = await supabase
        .from('messages')
        .insert({
          conversation_id: conversationId,
          sender,
          content,
          metadata
        })
        .select()
        .single()
      
      if (error) throw error
      return { data, error: null }
    } catch (error) {
      console.error('Add message error:', error)
      return { data: null, error }
    }
  },

  // Get RTI drafts
  async getRTIDrafts(userId) {
    try {
      const { data, error } = await supabase
        .from('rti_drafts')
        .select('*')
        .eq('user_id', userId)
        .order('created_at', { ascending: false })
      
      if (error) throw error
      return { data, error: null }
    } catch (error) {
      console.error('Get RTI drafts error:', error)
      return { data: null, error }
    }
  },

  // Create RTI draft
  async createRTIDraft(userId, title, content, department = null, subject = null) {
    try {
      const { data, error } = await supabase
        .from('rti_drafts')
        .insert({
          user_id: userId,
          title,
          content,
          department,
          subject
        })
        .select()
        .single()
      
      if (error) throw error
      return { data, error: null }
    } catch (error) {
      console.error('Create RTI draft error:', error)
      return { data: null, error }
    }
  }
}
