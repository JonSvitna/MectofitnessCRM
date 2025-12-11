-- Migration: Add theme_preference column to trainer_settings
-- This migration adds support for user-selectable light/dark themes

-- Add theme_preference column to trainer_settings table
ALTER TABLE trainer_settings 
ADD COLUMN IF NOT EXISTS theme_preference VARCHAR(10) DEFAULT 'light';

-- Add comment to document the column
COMMENT ON COLUMN trainer_settings.theme_preference IS 
'User theme preference: light, dark, or auto (follows system preference)';

-- Update existing rows to have default 'light' theme
UPDATE trainer_settings 
SET theme_preference = 'light' 
WHERE theme_preference IS NULL;
