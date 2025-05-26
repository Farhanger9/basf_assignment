import React, { useEffect, useState } from 'react';
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    TablePagination,
    Typography,
    Link,
    CircularProgress,
    Box,
} from '@mui/material';
const API_URL="http://127.0.0.1:5000";

const ViewFeedback = () => {
    const [feedbacks, setFeedbacks] = useState([]);
    const [loading, setLoading] = useState(true);

    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(5);

    const fetchFeedbacks = async () => {
        try {
            const res = await fetch(`${API_URL}/feedback`);
            const data = await res.json();
            setFeedbacks(data);
        } catch (err) {
            console.error('Error fetching feedbacks:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchFeedbacks();
    }, []);

    const handleChangePage = (event, newPage) => setPage(newPage);
    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    return (
        <Box sx={{ width: '95%', mx: 'auto', mt: 4 }}>
            <Typography
                variant="h4"
                align="center"
                gutterBottom
                sx={{
                    fontWeight: 600,
                    color: '#1976d2',
                    mb: 3,
                }}
            >
                Feedback Submission History
            </Typography>

            <Paper elevation={4} sx={{ p: 3 }}>
                {loading ? (
                    <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
                        <CircularProgress />
                    </Box>
                ) : (
                    <>
                        <TableContainer>
                            <Table>
                                <TableHead>
                                    <TableRow>
                                        <TableCell><strong>ID</strong></TableCell>
                                        <TableCell><strong>Feedback</strong></TableCell>
                                        <TableCell><strong>Sentiment</strong></TableCell>
                                        <TableCell><strong>Audio</strong></TableCell>
                                        <TableCell><strong>Submitted At</strong></TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {feedbacks
                                        .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                                        .map((row) => (
                                            <TableRow key={row.id}>
                                                <TableCell>{row.id}</TableCell>
                                                <TableCell>{row.feedback}</TableCell>
                                                <TableCell>{row.analysis?.[0]?.sentiment || 'N/A'}</TableCell>
                                                <TableCell>
                                                    <Link
                                                        href={`${API_URL}/${row.audio_file_path}`}
                                                        target="_blank"
                                                        rel="noopener"
                                                        download
                                                    >
                                                        Download
                                                    </Link>
                                                </TableCell>
                                                <TableCell>
                                                    {new Date(row.created_at).toLocaleString()}
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                </TableBody>
                            </Table>
                        </TableContainer>

                        <TablePagination
                            component="div"
                            count={feedbacks.length}
                            page={page}
                            onPageChange={handleChangePage}
                            rowsPerPage={rowsPerPage}
                            onRowsPerPageChange={handleChangeRowsPerPage}
                            rowsPerPageOptions={[5, 10, 25]}
                        />
                    </>
                )}
            </Paper>
        </Box>
    );
};

export default ViewFeedback;
