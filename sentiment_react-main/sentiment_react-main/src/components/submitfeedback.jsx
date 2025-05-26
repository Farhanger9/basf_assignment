import React, { useState } from 'react';
import {
    Grid,
    TextField,
    Button,
    CircularProgress,
    Typography,
    Paper,
} from '@mui/material';
const API_URL="http://127.0.0.1:5000/analyze";
const SubmitFeedback = () => {
    const [feedback, setFeedback] = useState('');
    const [response, setResponse] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setResponse('');
        setLoading(true);

        try {
            const res = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ content: feedback }),
            });

            const data = await res.json();
            if (data?.response_to_user) {
                setResponse(data.response_to_user);
            } else {
                setResponse('Thank you! We received your feedback.');
            }
            setFeedback('')
        } catch (err) {
            setResponse('An error occurred. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (

        <>

            <Grid
                container
                offset={8}
                size={6}
                sx={{
                    justifyContent: 'center',
                    alignItems: 'center',
                    marginTop:"200px"
                }}
            >
                <Grid item>
                    <Paper elevation={6} sx={{ p: 4, width: 400 }}>
                        <Typography variant="h4" align="center" gutterBottom>
                            Submit Your Feedback
                        </Typography>

                        {response && (
                            <Paper elevation={1} sx={{ p: 2, mb: 3, backgroundColor: '#e3f2fd' }}>
                                <Typography variant="subtitle1" color="primary" gutterBottom>
                                    Response:
                                </Typography>
                                <Typography>{response}</Typography>
                            </Paper>
                        )}

                        <form onSubmit={handleSubmit}>
                            <TextField
                                label="Your Feedback"
                                variant="outlined"
                                fullWidth
                                required
                                value={feedback}
                                onChange={(e) => setFeedback(e.target.value)}
                                multiline
                                rows={4}
                                sx={{ mb: 3 }}
                            />

                            <Button
                                type="submit"
                                variant="contained"
                                color="primary"
                                disabled={loading}
                                fullWidth
                            >
                                {loading ? <CircularProgress size={24} color="inherit" /> : 'Submit Feedback'}
                            </Button>
                        </form>
                    </Paper>
                </Grid>
            </Grid>
        </>


    );
};

export default SubmitFeedback;
