import { useState } from 'react'
import { 
  Container, 
  Box, 
  Typography, 
  Button, 
  LinearProgress,
  Paper,
  ThemeProvider,
  createTheme
} from '@mui/material'
import CloudUploadIcon from '@mui/icons-material/CloudUpload'
import axios from 'axios'
import type { AxiosProgressEvent } from 'axios'
import ResumeList from './components/ResumeList'
import './App.css'

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
})

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [isUploading, setIsUploading] = useState(false)

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0]
      if (file.type === 'application/pdf') {
        setSelectedFile(file)
        // Automatically start upload when file is selected
        await handleUpload(file)
      } else {
        alert('Please select a PDF file')
      }
    }
  }

  const handleUpload = async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)

    setIsUploading(true)
    setUploadProgress(0)

    try {
      await axios.post('/process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent: AxiosProgressEvent) => {
          const progress = progressEvent.total
            ? Math.round((progressEvent.loaded * 100) / progressEvent.total)
            : 0
          setUploadProgress(progress)
        },
      })
      alert('Resume uploaded successfully!')
    } catch (error) {
      console.error('Error uploading file:', error)
      alert('Error uploading file. Please try again.')
    } finally {
      setIsUploading(false)
      setSelectedFile(null)
    }
  }

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="md">
        <Box sx={{ my: 4, textAlign: 'center' }}>
          <Typography variant="h3" component="h1" gutterBottom>
            Resume Classification
          </Typography>
          <Paper 
            elevation={3} 
            sx={{ 
              p: 4, 
              mt: 4, 
              display: 'flex', 
              flexDirection: 'column', 
              alignItems: 'center',
              gap: 2,
              backgroundColor: 'background.paper'
            }}
          >
            <input
              accept=".pdf"
              style={{ display: 'none' }}
              id="resume-upload"
              type="file"
              onChange={handleFileSelect}
            />
            <label htmlFor="resume-upload">
              <Button
                variant="contained"
                component="span"
                startIcon={<CloudUploadIcon />}
                disabled={isUploading}
              >
                Select Resume
              </Button>
            </label>

            {selectedFile && (
              <Typography variant="body1">
                Selected file: {selectedFile.name}
              </Typography>
            )}

            {isUploading && (
              <Box sx={{ width: '100%', mt: 2 }}>
                <LinearProgress variant="determinate" value={uploadProgress} />
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                  Uploading: {uploadProgress}%
                </Typography>
              </Box>
            )}
          </Paper>

          <ResumeList />
        </Box>
      </Container>
    </ThemeProvider>
  )
}

export default App
