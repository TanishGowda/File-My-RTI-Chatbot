// Authentication context for managing user state
import React, { createContext, useContext, useEffect, useState } from 'react'
import { auth, db } from '../lib/supabase'

const AuthContext = createContext({})

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let mounted = true

    // Get initial session
    const getInitialSession = async () => {
      try {
        console.log('Getting initial session...')
        
        const { data: { session } } = await auth.getCurrentUser()
        
        console.log('Session data:', session)
        if (mounted) {
          if (session?.user) {
            setUser(session.user)
            // Load profile in background, don't wait for it
            loadUserProfile(session.user.id).catch(err => 
              console.error('Profile loading failed:', err)
            )
          }
          setLoading(false)
        }
      } catch (error) {
        console.error('Error getting initial session:', error)
        if (mounted) {
          setError(error.message)
          setLoading(false)
        }
      }
    }

    // Listen for auth state changes first
    const { data: { subscription } } = auth.onAuthStateChange(async (event, session) => {
      console.log('Auth state change:', event, session)
      if (mounted) {
        if (session?.user) {
          console.log('Setting user:', session.user)
          setUser(session.user)
          // Load profile in background, don't wait for it
          loadUserProfile(session.user.id).catch(err => 
            console.error('Profile loading failed:', err)
          )
        } else {
          console.log('No user in session, clearing user state')
          setUser(null)
          setProfile(null)
        }
        setLoading(false)
      }
    })

    // Then get initial session
    getInitialSession()

    return () => {
      mounted = false
      subscription.unsubscribe()
    }
  }, [])

  const loadUserProfile = async (userId) => {
    try {
      console.log('Loading profile for user:', userId)
      
      // Add timeout to prevent hanging
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Profile loading timeout')), 5000)
      )
      
      const profilePromise = db.getProfile(userId)
      
      const { data, error } = await Promise.race([profilePromise, timeoutPromise])
      
      if (error) {
        console.log('Profile not found, creating new one...')
        // Create profile if it doesn't exist
        const { data: newProfile } = await db.createProfile(
          userId,
          user?.email || 'user@example.com',
          user?.user_metadata?.full_name || 'User'
        )
        setProfile(newProfile)
      } else {
        console.log('Profile loaded:', data)
        setProfile(data)
      }
    } catch (error) {
      console.error('Error loading user profile:', error)
      // Don't block the app if profile loading fails
      console.log('Continuing without profile...')
    }
  }

  const signUp = async (email, password, fullName) => {
    try {
      setLoading(true)
      const { data, error } = await auth.signUp(email, password, fullName)
      if (error) throw error
      return { data, error: null }
    } catch (error) {
      return { data: null, error }
    } finally {
      setLoading(false)
    }
  }

  const signIn = async (email, password) => {
    try {
      setLoading(true)
      const { data, error } = await auth.signIn(email, password)
      if (error) throw error
      return { data, error: null }
    } catch (error) {
      return { data: null, error }
    } finally {
      setLoading(false)
    }
  }

  const signInWithGoogle = async () => {
    try {
      setLoading(true)
      const { data, error } = await auth.signInWithGoogle()
      if (error) throw error
      return { data, error: null }
    } catch (error) {
      return { data: null, error }
    } finally {
      setLoading(false)
    }
  }

  const signOut = async () => {
    try {
      setLoading(true)
      const { error } = await auth.signOut()
      if (error) throw error
      setUser(null)
      setProfile(null)
      return { error: null }
    } catch (error) {
      return { error }
    } finally {
      setLoading(false)
    }
  }

  const updateProfile = async (updates) => {
    try {
      if (!user) throw new Error('No user logged in')
      
      const { data, error } = await db.updateProfile(user.id, updates)
      if (error) throw error
      
      setProfile(data)
      return { data, error: null }
    } catch (error) {
      return { data: null, error }
    }
  }

  const value = {
    user,
    profile,
    loading,
    error,
    signUp,
    signIn,
    signInWithGoogle,
    signOut,
    updateProfile
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
