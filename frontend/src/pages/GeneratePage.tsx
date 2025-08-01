import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Typography,
  Paper,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  Chip,
  Grid,
  Alert,
} from '@mui/material';
import { useMutation, useQuery } from 'react-query';
import { transcribeVideo, getTranscriptionStatus, getTranscriptionResult } from '../services/api';

interface Segment {
  timestamp: number;
  text: string;
}

const GeneratePage: React.FC = () => {
  const [url, setUrl] = useState('');
  const [topics, setTopics] = useState('');
  const [title, setTitle] = useState('');
  const [tags, setTags] = useState('');
  const [jobId, setJobId] = useState<string | null>(null);
  const [segments, setSegments] = useState<Segment[]>([]);

  const transcribeMutation = useMutation(transcribeVideo, {
    onSuccess: (data) => {
      setJobId(data.jobId);
    },
    onError: (error) => {
      console.error('Transcription failed:', error);
    },
  });

  const statusQuery = useQuery(
    ['transcription-status', jobId],
    () => getTranscriptionStatus(jobId!),
    {
      enabled: !!jobId,
      refetchInterval: (data) => (data?.status === 'completed' ? false : 2000),
      onSuccess: (data) => {
        if (data.status === 'completed') {
          resultQuery.refetch();
        }
      },
    }
  );

  const resultQuery = useQuery(
    ['transcription-result', jobId],
    () => getTranscriptionResult(jobId!, topics.split(',').map(t => t.trim())),
    {
      enabled: !!jobId && statusQuery.data?.status === 'completed',
      onSuccess: (data) => {
        setSegments(data.segments);
      },
    }
  );

  const handleTranscribe = () => {
    if (!url.trim()) return;
    transcribeMutation.mutate({ url, topics: topics.split(',').map(t => t.trim()) });
  };

  const handleSave = async () => {
    if (!title.trim() || segments.length === 0) return;
    
    try {
      await fetch('/api/notes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title,
          tags: tags.split(',').map(t => t.trim()),
          segments,
          sourceUrl: url,
        }),
      });
      
      // Reset form
      setTitle('');
      setTags('');
      setSegments([]);
      setJobId(null);
    } catch (error) {
      console.error('Failed to save note:', error);
    }
  };

  const isTranscribing = statusQuery.data?.status === 'processing';
  const isCompleted = statusQuery.data?.status === 'completed';

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Generate Transcription
      </Typography>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Video URL (YouTube or other video platform)"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://www.youtube.com/watch?v=..."
              disabled={isTranscribing}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Topics (comma-separated)"
              value={topics}
              onChange={(e) => setTopics(e.target.value)}
              placeholder="AI, machine learning, programming"
              disabled={isTranscribing}
              helperText="Enter keywords to filter the transcription"
            />
          </Grid>
          <Grid item xs={12}>
            <Button
              variant="contained"
              onClick={handleTranscribe}
              disabled={!url.trim() || isTranscribing}
              size="large"
            >
              Start Transcription
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {isTranscribing && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Transcribing...
          </Typography>
          <LinearProgress />
          <Typography variant="body2" sx={{ mt: 1 }}>
            Progress: {statusQuery.data?.progress || 0}%
          </Typography>
        </Paper>
      )}

      {isCompleted && segments.length > 0 && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Filtered Segments
          </Typography>
          <List>
            {segments.map((segment, index) => (
              <ListItem key={index} divider>
                <ListItemText
                  primary={segment.text}
                  secondary={`${Math.floor(segment.timestamp / 60)}:${(segment.timestamp % 60).toString().padStart(2, '0')}`}
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}

      {isCompleted && segments.length > 0 && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Save Note
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter a title for your note"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Tags (comma-separated)"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
                placeholder="AI, tutorial, notes"
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                variant="contained"
                onClick={handleSave}
                disabled={!title.trim()}
                color="secondary"
              >
                Save Note
              </Button>
            </Grid>
          </Grid>
        </Paper>
      )}

      {transcribeMutation.isError && (
        <Alert severity="error" sx={{ mt: 2 }}>
          Failed to start transcription. Please try again.
        </Alert>
      )}
    </Box>
  );
};

export default GeneratePage; 