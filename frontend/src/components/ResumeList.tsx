import { useState, useEffect, forwardRef, useImperativeHandle } from 'react';
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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  InputAdornment,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
} from '@mui/material';
import type { SelectChangeEvent } from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';
import SettingsIcon from '@mui/icons-material/Settings';
import axios from 'axios';

interface Candidate {
  id: string;
  name: string;
  skills: string[];
  fe_score: number;
  be_score: number;
  seniority: string;
  qualifications: string;
  created_at: string;
  updated_at: string;
}

interface FilterSettings {
  skills: string[];
  seniorityLevel: string | null;
  qualifications: string | null;
  fe_score: number | null;
  be_score: number | null;
}

const defaultFilterSettings: FilterSettings = {
  skills: [],
  seniorityLevel: null,
  qualifications: null,
  fe_score: null,
  be_score: null,
};

const getJobRole = (feScore: number, beScore: number): string => {
  if (feScore >= 50 && beScore >= 50) return 'FullStack';
  if (beScore >= 50) return 'Backend';
  if (feScore >= 50) return 'Frontend';
  return 'Other';
};

export interface ResumeListRef {
  fetchCandidates: () => void;
}

const ResumeList = forwardRef<ResumeListRef>((_, ref) => {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [page, setPage] = useState(1);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState<FilterSettings>(() => {
    const savedSettings = localStorage.getItem('resumeFilterSettings');
    return savedSettings ? JSON.parse(savedSettings) : defaultFilterSettings;
  });
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [tempSettings, setTempSettings] = useState<FilterSettings>(filters);

  const fetchCandidates = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/get-candidates/', {
        page,
        skills: filters.skills,
        seniorityLevel: filters.seniorityLevel,
        qualifications: filters.qualifications,
        fe_score: filters.fe_score,
        be_score: filters.be_score,
      });
      setCandidates(response.data.candidates);
      setTotalCount(response.data.total_count);
    } catch (error) {
      console.error('Error fetching candidates:', error);
    } finally {
      setLoading(false);
    }
  };

  useImperativeHandle(ref, () => ({
    fetchCandidates,
  }));

  useEffect(() => {
    fetchCandidates();
  }, [page, filters]);

  useEffect(() => {
    localStorage.setItem('resumeFilterSettings', JSON.stringify(filters));
  }, [filters]);

  const handleSeniorityChange = (event: SelectChangeEvent) => {
    setFilters(prev => ({
      ...prev,
      seniorityLevel: event.target.value || null,
    }));
  };

  const handleQualificationsChange = (event: SelectChangeEvent) => {
    setFilters(prev => ({
      ...prev,
      qualifications: event.target.value || null,
    }));
  };

  const handleSettingsOpen = () => {
    setTempSettings(filters);
    setSettingsOpen(true);
  };

  const handleSettingsClose = () => {
    setSettingsOpen(false);
  };

  const handleSettingsSave = () => {
    setFilters(tempSettings);
    setSettingsOpen(false);
  };

  const handleTempScoreChange = (param: 'fe_score' | 'be_score') => 
    (_event: Event, newValue: number | number[]) => {
      setTempSettings(prev => ({
        ...prev,
        [param]: newValue as number,
      }));
    };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <Box sx={{ mt: 2 }}>
      <Paper elevation={3} sx={{ p: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1, px: 1 }}>
          <Typography variant="h5" gutterBottom sx={{ mb: 0 }}>
            Candidate List
          </Typography>
          <Tooltip title="Threshold Settings">
            <IconButton onClick={handleSettingsOpen} size="small">
              <SettingsIcon />
            </IconButton>
          </Tooltip>
        </Box>

        <Grid container spacing={1} sx={{ mb: 1, px: 1 }}>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth size="small">
              <InputLabel>Seniority Level</InputLabel>
              <Select
                value={filters.seniorityLevel || ''}
                onChange={handleSeniorityChange}
                label="Seniority Level"
              >
                <MenuItem value="">All</MenuItem>
                <MenuItem value="junior">Junior</MenuItem>
                <MenuItem value="senior">Senior</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} md={6}>
            <FormControl fullWidth size="small">
              <InputLabel>Qualifications</InputLabel>
              <Select
                value={filters.qualifications || ''}
                onChange={handleQualificationsChange}
                label="Qualifications"
              >
                <MenuItem value="">All</MenuItem>
                <MenuItem value="bachelors">Bachelor's</MenuItem>
                <MenuItem value="masters">Master's</MenuItem>
                <MenuItem value="phd">PhD</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>

        {loading ? (
          <Typography>Loading...</Typography>
        ) : (
          <>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell padding="checkbox">Name</TableCell>
                    <TableCell padding="checkbox">Role</TableCell>
                    <TableCell padding="checkbox">Skills</TableCell>
                    <TableCell padding="checkbox" align="center">Frontend</TableCell>
                    <TableCell padding="checkbox" align="center">Backend</TableCell>
                    <TableCell padding="checkbox">Seniority</TableCell>
                    <TableCell padding="checkbox">Qualifications</TableCell>
                    <TableCell padding="checkbox">Uploaded</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {candidates.map((candidate) => (
                    <TableRow key={candidate.id}>
                      <TableCell padding="checkbox">{candidate.name}</TableCell>
                      <TableCell padding="checkbox">
                        <Chip
                          label={getJobRole(candidate.fe_score, candidate.be_score)}
                          size="small"
                          color={getJobRole(candidate.fe_score, candidate.be_score) === 'FullStack' ? 'primary' : 'default'}
                          variant={getJobRole(candidate.fe_score, candidate.be_score) === 'FullStack' ? 'filled' : 'outlined'}
                        />
                      </TableCell>
                      <TableCell padding="checkbox">
                        <Stack direction="row" spacing={0.5} flexWrap="wrap" useFlexGap>
                          {candidate.skills.slice(0, 3).map((skill) => (
                            <Chip
                              key={skill}
                              label={skill}
                              size="small"
                              sx={{ m: 0.25 }}
                            />
                          ))}
                          {candidate.skills.length > 3 && (
                            <Chip
                              label={`+${candidate.skills.length - 3} more`}
                              size="small"
                              sx={{ m: 0.25 }}
                              color="default"
                              variant="outlined"
                            />
                          )}
                        </Stack>
                      </TableCell>
                      <TableCell padding="checkbox" align="center">
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                          <Box
                            sx={{
                              width: 32,
                              height: 32,
                              borderRadius: '50%',
                              bgcolor: candidate.fe_score >= 50 ? 'success.main' : 'warning.main',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              color: 'white',
                              fontWeight: 'bold',
                              fontSize: '0.75rem',
                            }}
                          >
                            {candidate.fe_score}%
                          </Box>
                        </Box>
                      </TableCell>
                      <TableCell padding="checkbox" align="center">
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                          <Box
                            sx={{
                              width: 32,
                              height: 32,
                              borderRadius: '50%',
                              bgcolor: candidate.be_score >= 50 ? 'success.main' : 'warning.main',
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              color: 'white',
                              fontWeight: 'bold',
                              fontSize: '0.75rem',
                            }}
                          >
                            {candidate.be_score}%
                          </Box>
                        </Box>
                      </TableCell>
                      <TableCell padding="checkbox" sx={{ textTransform: 'capitalize' }}>
                        {candidate.seniority}
                      </TableCell>
                      <TableCell padding="checkbox" sx={{ textTransform: 'capitalize' }}>
                        {candidate.qualifications}
                      </TableCell>
                      <TableCell padding="checkbox">{formatDate(candidate.created_at)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>

            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 1 }}>
              <Pagination
                count={Math.ceil(totalCount / 10)}
                page={page}
                onChange={(_, value) => setPage(value)}
                color="primary"
                showFirstButton
                showLastButton
                size="small"
              />
            </Box>
          </>
        )}

        <Dialog open={settingsOpen} onClose={handleSettingsClose} maxWidth="sm" fullWidth>
          <DialogTitle>Threshold Settings</DialogTitle>
          <DialogContent>
            <Box sx={{ mt: 2 }}>
              <Typography gutterBottom>Frontend Score Threshold</Typography>
              <Slider
                value={tempSettings.fe_score || 0}
                onChange={handleTempScoreChange('fe_score')}
                valueLabelDisplay="auto"
                min={0}
                max={100}
                marks={[
                  { value: 0, label: '0%' },
                  { value: 50, label: '50%' },
                  { value: 100, label: '100%' },
                ]}
              />
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Minimum frontend skills score required for candidates
              </Typography>
            </Box>
            <Box sx={{ mt: 4 }}>
              <Typography gutterBottom>Backend Score Threshold</Typography>
              <Slider
                value={tempSettings.be_score || 0}
                onChange={handleTempScoreChange('be_score')}
                valueLabelDisplay="auto"
                min={0}
                max={100}
                marks={[
                  { value: 0, label: '0%' },
                  { value: 50, label: '50%' },
                  { value: 100, label: '100%' },
                ]}
              />
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Minimum backend skills score required for candidates
              </Typography>
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleSettingsClose}>Cancel</Button>
            <Button onClick={handleSettingsSave} variant="contained">Save</Button>
          </DialogActions>
        </Dialog>
      </Paper>
    </Box>
  );
});

export default ResumeList; 