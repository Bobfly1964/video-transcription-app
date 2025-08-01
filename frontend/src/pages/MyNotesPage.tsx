import React from 'react';
import {
  Box,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemText,
  Chip,
  Button,
  Grid,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';
import { Edit, Delete, Visibility } from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { getNotes, deleteNote, updateNote, Note } from '../services/api';

const MyNotesPage: React.FC = () => {
  const [selectedNote, setSelectedNote] = React.useState<Note | null>(null);
  const [editDialogOpen, setEditDialogOpen] = React.useState(false);
  const [viewDialogOpen, setViewDialogOpen] = React.useState(false);
  const [editTitle, setEditTitle] = React.useState('');
  const [editTags, setEditTags] = React.useState('');

  const queryClient = useQueryClient();

  const { data: notes = [], isLoading, error } = useQuery('notes', getNotes);

  const deleteMutation = useMutation(deleteNote, {
    onSuccess: () => {
      queryClient.invalidateQueries('notes');
    },
  });

  const updateMutation = useMutation(
    ({ id, data }: { id: string; data: Partial<Note> }) => updateNote(id, data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('notes');
        setEditDialogOpen(false);
      },
    }
  );

  const handleEdit = (note: Note) => {
    setSelectedNote(note);
    setEditTitle(note.title);
    setEditTags(note.tags.join(', '));
    setEditDialogOpen(true);
  };

  const handleView = (note: Note) => {
    setSelectedNote(note);
    setViewDialogOpen(true);
  };

  const handleDelete = (id: string) => {
    if (window.confirm('Are you sure you want to delete this note?')) {
      deleteMutation.mutate(id);
    }
  };

  const handleSaveEdit = () => {
    if (selectedNote) {
      updateMutation.mutate({
        id: selectedNote.id,
        data: {
          title: editTitle,
          tags: editTags.split(',').map(t => t.trim()),
        },
      });
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  if (isLoading) {
    return (
      <Box>
        <Typography variant="h4" gutterBottom>
          My Notes
        </Typography>
        <Typography>Loading...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box>
        <Typography variant="h4" gutterBottom>
          My Notes
        </Typography>
        <Typography color="error">Failed to load notes</Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        My Notes
      </Typography>

      {notes.length === 0 ? (
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography variant="h6" color="textSecondary">
            No notes yet. Start by generating a transcription!
          </Typography>
        </Paper>
      ) : (
        <List>
          {notes.map((note) => (
            <Paper key={note.id} sx={{ mb: 2 }}>
              <ListItem>
                <ListItemText
                  primary={note.title}
                  secondary={
                    <Box>
                      <Typography variant="body2" color="textSecondary">
                        Created: {formatDate(note.createdAt)}
                      </Typography>
                      <Box sx={{ mt: 1 }}>
                        {note.tags.map((tag) => (
                          <Chip
                            key={tag}
                            label={tag}
                            size="small"
                            sx={{ mr: 0.5, mb: 0.5 }}
                          />
                        ))}
                      </Box>
                      <Typography variant="body2" color="textSecondary">
                        {note.segments.length} segments
                      </Typography>
                    </Box>
                  }
                />
                <Box>
                  <IconButton onClick={() => handleView(note)}>
                    <Visibility />
                  </IconButton>
                  <IconButton onClick={() => handleEdit(note)}>
                    <Edit />
                  </IconButton>
                  <IconButton onClick={() => handleDelete(note.id)} color="error">
                    <Delete />
                  </IconButton>
                </Box>
              </ListItem>
            </Paper>
          ))}
        </List>
      )}

      {/* Edit Dialog */}
      <Dialog open={editDialogOpen} onClose={() => setEditDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Edit Note</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            label="Title"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            sx={{ mt: 2 }}
          />
          <TextField
            fullWidth
            label="Tags (comma-separated)"
            value={editTags}
            onChange={(e) => setEditTags(e.target.value)}
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSaveEdit} variant="contained">
            Save
          </Button>
        </DialogActions>
      </Dialog>

      {/* View Dialog */}
      <Dialog open={viewDialogOpen} onClose={() => setViewDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>{selectedNote?.title}</DialogTitle>
        <DialogContent>
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              Tags:
            </Typography>
            <Box>
              {selectedNote?.tags.map((tag) => (
                <Chip key={tag} label={tag} size="small" sx={{ mr: 0.5, mb: 0.5 }} />
              ))}
            </Box>
          </Box>
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" gutterBottom>
              Source URL:
            </Typography>
            <Typography variant="body2" color="textSecondary">
              {selectedNote?.sourceUrl}
            </Typography>
          </Box>
          <Box>
            <Typography variant="subtitle2" gutterBottom>
              Segments:
            </Typography>
            <List dense>
              {selectedNote?.segments.map((segment, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={segment.text}
                    secondary={`${Math.floor(segment.timestamp / 60)}:${(segment.timestamp % 60).toString().padStart(2, '0')}`}
                  />
                </ListItem>
              ))}
            </List>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setViewDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default MyNotesPage; 