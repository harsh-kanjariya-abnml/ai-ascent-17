import { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Pagination,
  Slider,
  Grid,
  Chip,
  Stack,
} from '@mui/material';
import type { SelectChangeEvent } from '@mui/material';
import axios from 'axios';

interface Candidate {
  id: string;
  name: string;
  jobRole: string;
  seniorityLevel: string;
  frontendScore: number;
  backendScore: number;
}

interface FilterSettings {
  jobRoles: string[];
  seniorityLevels: string[];
  frontendThreshold: number;
  backendThreshold: number;
}

const defaultFilterSettings: FilterSettings = {
  jobRoles: ['FullStack', 'Backend'],
  seniorityLevels: ['Junior Software Engineer', 'Senior Software Engineer'],
  frontendThreshold: 50,
  backendThreshold: 50,
};

export default function ResumeList() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState<FilterSettings>(() => {
    const savedSettings = localStorage.getItem('resumeFilterSettings');
    return savedSettings ? JSON.parse(savedSettings) : defaultFilterSettings;
  });

  const fetchCandidates = async () => {
    setLoading(true);
    try {
      const response = await axios.post('/get-candidates', {
        page,
        filters,
      });
      setCandidates(response.data.candidates);
      setTotalPages(response.data.totalPages);
    } catch (error) {
      console.error('Error fetching candidates:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCandidates();
  }, [page, filters]);

  useEffect(() => {
    localStorage.setItem('resumeFilterSettings', JSON.stringify(filters));
  }, [filters]);

  const handleJobRoleChange = (event: SelectChangeEvent<string[]>) => {
    setFilters(prev => ({
      ...prev,
      jobRoles: event.target.value as string[],
    }));
  };

  const handleSeniorityChange = (event: SelectChangeEvent<string[]>) => {
    setFilters(prev => ({
      ...prev,
      seniorityLevels: event.target.value as string[],
    }));
  };

  const handleThresholdChange = (param: 'frontendThreshold' | 'backendThreshold') => 
    (_event: Event, newValue: number | number[]) => {
      setFilters(prev => ({
        ...prev,
        [param]: newValue as number,
      }));
    };

  return (
    <Box sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Candidate List
        </Typography>

        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Job Roles</InputLabel>
              <Select
                multiple
                value={filters.jobRoles}
                onChange={handleJobRoleChange}
                renderValue={(selected) => (
                  <Stack direction="row" spacing={1}>
                    {selected.map((value) => (
                      <Chip key={value} label={value} />
                    ))}
                  </Stack>
                )}
              >
                <MenuItem value="FullStack">FullStack</MenuItem>
                <MenuItem value="Backend">Backend</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Seniority Level</InputLabel>
              <Select
                multiple
                value={filters.seniorityLevels}
                onChange={handleSeniorityChange}
                renderValue={(selected) => (
                  <Stack direction="row" spacing={1}>
                    {selected.map((value) => (
                      <Chip key={value} label={value} />
                    ))}
                  </Stack>
                )}
              >
                <MenuItem value="Junior Software Engineer">Junior Software Engineer</MenuItem>
                <MenuItem value="Senior Software Engineer">Senior Software Engineer</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography gutterBottom>Frontend Score Threshold</Typography>
            <Slider
              value={filters.frontendThreshold}
              onChange={handleThresholdChange('frontendThreshold')}
              valueLabelDisplay="auto"
              min={0}
              max={100}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <Typography gutterBottom>Backend Score Threshold</Typography>
            <Slider
              value={filters.backendThreshold}
              onChange={handleThresholdChange('backendThreshold')}
              valueLabelDisplay="auto"
              min={0}
              max={100}
            />
          </Grid>
        </Grid>

        {loading ? (
          <Typography>Loading...</Typography>
        ) : (
          <>
            <Box sx={{ mb: 2 }}>
              {candidates.map((candidate) => (
                <Paper
                  key={candidate.id}
                  elevation={1}
                  sx={{ p: 2, mb: 2 }}
                >
                  <Typography variant="h6">{candidate.name}</Typography>
                  <Typography color="text.secondary">
                    {candidate.jobRole} - {candidate.seniorityLevel}
                  </Typography>
                  <Box sx={{ mt: 1 }}>
                    <Typography variant="body2">
                      Frontend Score: {candidate.frontendScore}%
                    </Typography>
                    <Typography variant="body2">
                      Backend Score: {candidate.backendScore}%
                    </Typography>
                  </Box>
                </Paper>
              ))}
            </Box>

            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
              <Pagination
                count={totalPages}
                page={page}
                onChange={(_, value) => setPage(value)}
                color="primary"
              />
            </Box>
          </>
        )}
      </Paper>
    </Box>
  );
} 