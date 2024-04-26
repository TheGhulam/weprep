import React, { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import {
  Paper,
  Grid,
  Card,
  CardActions,
  CardContent,
  Button,
  Typography,
  Box,
  IconButton,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import FileDownloadIcon from "@mui/icons-material/FileDownload";
import InsertDriveFileIcon from "@mui/icons-material/InsertDriveFile";
import { Document, Page, pdfjs } from "react-pdf";
import "react-pdf/dist/esm/Page/AnnotationLayer.css";

// Configure pdfjs worker
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

const resumes = [
  {
    id: 1,
    title: "Software Engineer Resume",
    path: "resume1.pdf",
  },
  {
    id: 2,
    title: "Project Manager Resume",
    path: "resume2.pdf",
  },
];

const ResumePage = () => {
  const onDrop = useCallback((acceptedFiles) => {
    console.log(acceptedFiles);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  const handleDelete = (id) => {
    console.log("Delete resume with id:", id);
  };

  const handleEdit = (id) => {
    console.log("Edit resume with id:", id);
  };

  const handleDownload = (path) => {
    window.open(path);
  };

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Typography variant="h2" align="center" gutterBottom>
        Resumes
      </Typography>
      <Grid container spacing={3}>
        {resumes.map((resume) => (
          <Grid item key={resume.id} xs={12} sm={6} md={3}>
            <Card>
              <CardContent sx={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                <Typography variant="h3" component="div" align="center" marginBottom={1}>
                  {resume.title}
                </Typography>
                <Document file={resume.path}>
                  <Page pageNumber={1} width={200} height={200} />
                </Document>
              </CardContent>
              <CardActions sx={{ justifyContent: "center" }}>
                <Button size="small" onClick={() => handleEdit(resume.id)} startIcon={<EditIcon />}>
                  Edit
                </Button>
                <Button
                  size="small"
                  onClick={() => handleDelete(resume.id)}
                  startIcon={<DeleteIcon />}
                >
                  Delete
                </Button>
                <Button
                  size="small"
                  onClick={() => handleDownload(resume.path)}
                  startIcon={<FileDownloadIcon />}
                >
                  Download
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Paper
        variant="outlined"
        sx={{
          p: 3,
          mt: 5,
          textAlign: "center",
          position: "fixed",
          bottom: 20,
          left: 0,
          right: 0,
          ...(isDragActive && { bgcolor: "action.hover" }),
        }}
        {...getRootProps()}
      >
        <input {...getInputProps()} />
        <IconButton color="primary" sx={{ fontSize: 50 }}>
          <InsertDriveFileIcon sx={{ fontSize: 50 }} />
        </IconButton>
        {isDragActive ? (
          <Typography>Drop the resumes here ...</Typography>
        ) : (
          <Typography>Drag 'n' drop some resumes here, or click to select resumes</Typography>
        )}
      </Paper>
    </Box>
  );
};

export default ResumePage;
