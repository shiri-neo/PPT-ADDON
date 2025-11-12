/**
 * Company Settings page - branding and configuration
 */

import React, { useEffect, useState } from 'react';
import apiClient from '../api/client';

interface OrganizationSettings {
  name: string;
  logo_url: string | null;
  primary_color: string;
  secondary_color: string;
  accent_color: string;
  font_family: string;
  design_style: string;
}

const CompanySettings: React.FC = () => {
  const [settings, setSettings] = useState<OrganizationSettings | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const response = await apiClient.get('/organization/settings');
      setSettings(response.data);
    } catch (err) {
      console.error('Failed to load settings:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!settings) return;

    setSaving(true);
    setMessage('');

    try {
      await apiClient.put('/organization/settings', settings);
      setMessage('Settings saved successfully!');
      setTimeout(() => setMessage(''), 3000);
    } catch (err: any) {
      setMessage(err.response?.data?.detail || 'Failed to save settings');
    } finally {
      setSaving(false);
    }
  };

  if (loading || !settings) {
    return <div style={styles.container}><p>Loading settings...</p></div>;
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Company Settings</h1>
      <p style={styles.subtitle}>Customize your brand and presentation style</p>

      {message && (
        <div style={message.includes('success') ? styles.success : styles.error}>
          {message}
        </div>
      )}

      <div style={styles.form}>
        {/* Company Name */}
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Company Information</h2>

          <div style={styles.field}>
            <label style={styles.label}>Company Name</label>
            <input
              type="text"
              value={settings.name}
              onChange={(e) => setSettings({ ...settings, name: e.target.value })}
              style={styles.input}
            />
          </div>

          <div style={styles.field}>
            <label style={styles.label}>Logo URL (optional)</label>
            <input
              type="text"
              value={settings.logo_url || ''}
              onChange={(e) => setSettings({ ...settings, logo_url: e.target.value })}
              placeholder="https://example.com/logo.png"
              style={styles.input}
            />
            <span style={styles.helpText}>Enter a URL to your company logo</span>
          </div>
        </div>

        {/* Brand Colors */}
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Brand Colors</h2>

          <div style={styles.colorGrid}>
            <div style={styles.colorField}>
              <label style={styles.label}>Primary Color</label>
              <div style={styles.colorInputWrapper}>
                <input
                  type="color"
                  value={settings.primary_color}
                  onChange={(e) => setSettings({ ...settings, primary_color: e.target.value })}
                  style={styles.colorInput}
                />
                <input
                  type="text"
                  value={settings.primary_color}
                  onChange={(e) => setSettings({ ...settings, primary_color: e.target.value })}
                  style={styles.colorTextInput}
                  placeholder="#0078D4"
                />
              </div>
            </div>

            <div style={styles.colorField}>
              <label style={styles.label}>Secondary Color</label>
              <div style={styles.colorInputWrapper}>
                <input
                  type="color"
                  value={settings.secondary_color}
                  onChange={(e) => setSettings({ ...settings, secondary_color: e.target.value })}
                  style={styles.colorInput}
                />
                <input
                  type="text"
                  value={settings.secondary_color}
                  onChange={(e) => setSettings({ ...settings, secondary_color: e.target.value })}
                  style={styles.colorTextInput}
                  placeholder="#106EBE"
                />
              </div>
            </div>

            <div style={styles.colorField}>
              <label style={styles.label}>Accent Color</label>
              <div style={styles.colorInputWrapper}>
                <input
                  type="color"
                  value={settings.accent_color}
                  onChange={(e) => setSettings({ ...settings, accent_color: e.target.value })}
                  style={styles.colorInput}
                />
                <input
                  type="text"
                  value={settings.accent_color}
                  onChange={(e) => setSettings({ ...settings, accent_color: e.target.value })}
                  style={styles.colorTextInput}
                  placeholder="#00BCF2"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Design Preferences */}
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Design Preferences</h2>

          <div style={styles.field}>
            <label style={styles.label}>Font Family</label>
            <select
              value={settings.font_family}
              onChange={(e) => setSettings({ ...settings, font_family: e.target.value })}
              style={styles.select}
            >
              <option value="Arial">Arial</option>
              <option value="Calibri">Calibri</option>
              <option value="Times New Roman">Times New Roman</option>
              <option value="Helvetica">Helvetica</option>
              <option value="Georgia">Georgia</option>
              <option value="Verdana">Verdana</option>
            </select>
          </div>

          <div style={styles.field}>
            <label style={styles.label}>Design Style</label>
            <div style={styles.styleGrid}>
              {['professional', 'modern', 'creative', 'minimal'].map((style) => (
                <button
                  key={style}
                  onClick={() => setSettings({ ...settings, design_style: style })}
                  style={{
                    ...styles.styleButton,
                    ...(settings.design_style === style ? styles.styleButtonActive : {}),
                  }}
                >
                  {style.charAt(0).toUpperCase() + style.slice(1)}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Preview */}
        <div style={styles.section}>
          <h2 style={styles.sectionTitle}>Color Preview</h2>
          <div style={styles.preview}>
            <div style={{ ...styles.previewBox, backgroundColor: settings.primary_color }}>
              Primary
            </div>
            <div style={{ ...styles.previewBox, backgroundColor: settings.secondary_color }}>
              Secondary
            </div>
            <div style={{ ...styles.previewBox, backgroundColor: settings.accent_color }}>
              Accent
            </div>
          </div>
        </div>

        {/* Save Button */}
        <button
          onClick={handleSave}
          disabled={saving}
          style={styles.saveButton}
        >
          {saving ? 'Saving...' : 'Save Settings'}
        </button>
      </div>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    padding: '30px',
    maxWidth: '900px',
  },
  title: {
    fontSize: '32px',
    fontWeight: 700,
    margin: '0 0 10px 0',
  },
  subtitle: {
    fontSize: '16px',
    color: '#666',
    margin: '0 0 30px 0',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '30px',
  },
  section: {
    backgroundColor: 'white',
    padding: '24px',
    border: '1px solid #e0e0e0',
    borderRadius: '8px',
  },
  sectionTitle: {
    fontSize: '20px',
    fontWeight: 600,
    marginBottom: '20px',
    marginTop: 0,
  },
  field: {
    marginBottom: '20px',
  },
  label: {
    display: 'block',
    fontSize: '14px',
    fontWeight: 500,
    marginBottom: '8px',
  },
  input: {
    width: '100%',
    padding: '10px',
    fontSize: '14px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    boxSizing: 'border-box',
  },
  select: {
    width: '100%',
    padding: '10px',
    fontSize: '14px',
    border: '1px solid #ccc',
    borderRadius: '4px',
  },
  helpText: {
    display: 'block',
    fontSize: '12px',
    color: '#666',
    marginTop: '4px',
  },
  colorGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '16px',
  },
  colorField: {
    display: 'flex',
    flexDirection: 'column',
  },
  colorInputWrapper: {
    display: 'flex',
    gap: '8px',
    alignItems: 'center',
  },
  colorInput: {
    width: '50px',
    height: '40px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  colorTextInput: {
    flex: 1,
    padding: '8px',
    fontSize: '14px',
    border: '1px solid #ccc',
    borderRadius: '4px',
  },
  styleGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
    gap: '10px',
  },
  styleButton: {
    padding: '12px',
    backgroundColor: '#f5f5f5',
    border: '2px solid #e0e0e0',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: 500,
    transition: 'all 0.2s',
  },
  styleButtonActive: {
    backgroundColor: '#0078d4',
    color: 'white',
    borderColor: '#0078d4',
  },
  preview: {
    display: 'flex',
    gap: '16px',
  },
  previewBox: {
    flex: 1,
    padding: '30px 20px',
    color: 'white',
    textAlign: 'center',
    borderRadius: '6px',
    fontWeight: 600,
  },
  saveButton: {
    padding: '14px 30px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontSize: '16px',
    fontWeight: 600,
    cursor: 'pointer',
    alignSelf: 'flex-start',
  },
  success: {
    padding: '12px',
    backgroundColor: '#d4edda',
    color: '#155724',
    borderRadius: '6px',
    marginBottom: '20px',
  },
  error: {
    padding: '12px',
    backgroundColor: '#f8d7da',
    color: '#721c24',
    borderRadius: '6px',
    marginBottom: '20px',
  },
};

export default CompanySettings;
