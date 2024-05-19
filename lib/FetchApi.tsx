interface UploadResponse {
  task_id: string;
  status: string;
}

interface SummaryResponse {
  task_id: string;
  summary: string;
}

export const GetSummaryAPI = async (task_id: string): Promise<SummaryResponse> => {
  try {
    const response = await fetch(`http://localhost:3000/api/taskResult/${task_id}`, {
      method: "GET",
    });
    if (!response.ok) {
      throw new Error("Failed to get task result");
    }
    const data: SummaryResponse = await response.json();
    console.log(data);
    return data;
  } catch (error) {
    console.error("Error getting task result:", error);
    throw error;
  }
};

export const AddFileAPI = async (files: File): Promise<SummaryResponse> => {
  const formData = new FormData();
  formData.append("file", files);

  try {
    const response = await fetch(`http://localhost:3000/api/uploadFile`, {
      method: "POST",
      body: formData,
    });
    if (!response.ok) {
      throw new Error("Failed to upload files");
    }
    const data: UploadResponse = await response.json();
    console.log(data);
    
    // Wait for 10 seconds before calling GetSummaryAPI
    await new Promise(resolve => setTimeout(resolve, 10000));
    
    const newData = await GetSummaryAPI(data.task_id);
    console.log(newData);
    return newData;
  } catch (error) {
    console.error("Error uploading files:", error);
    throw error;
  }
};

// Uncomment the following code if you need chunked file uploads

// export const AddFileAPI = async (files: File): Promise<{ success: boolean }> => {
//   const CHUNK_SIZE = 1024 * 1024; // 1MB
//   const chunks: Blob[] = [];

//   for (let i = 0; i < files.size; i += CHUNK_SIZE) {
//     const chunk = files.slice(i, i + CHUNK_SIZE);
//     chunks.push(chunk);
//   }

//   const maxRetries = 5;
//   let retries = 0;

//   while (retries < maxRetries) {
//     try {
//       for (let i = 0; i < chunks.length; i++) {
//         const formData = new FormData();
//         formData.append("file", chunks[i]);

//         const response = await fetch(`http://localhost:3000/api/uploadFile`, {
//           method: "POST",
//           body: formData,
//         });

//         if (!response.ok) {
//           throw new Error("Failed to upload chunk");
//         }

//         console.log(`Chunk ${i + 1}/${chunks.length} uploaded successfully`);
//       }

//       console.log("All chunks uploaded successfully");
//       return { success: true };
//     } catch (error) {
//       console.error("Error uploading chunks:", error);
//       retries++;
//       const waitTime = 2 ** retries * 1000; // Exponential backoff
//       console.log(`Retrying in ${waitTime / 1000} seconds...`);
//       await new Promise((resolve) => setTimeout(resolve, waitTime));
//     }
//   }

//   throw new Error("Max retries exceeded. Unable to upload file.");
// };
