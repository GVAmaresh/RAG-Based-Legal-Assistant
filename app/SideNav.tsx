"use client";
import { useState, useRef } from "react";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import CssBaseline from "@mui/material/CssBaseline";
import Drawer from "@mui/material/Drawer";
import IconButton from "@mui/material/IconButton";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import MenuIcon from "@mui/icons-material/Menu";
import { AiFillFileAdd } from "react-icons/ai";
import Link from "next/link";
import { AddFileAPI } from "@/lib/FetchApi";
import { Provider, useDispatch } from "react-redux";
import store from "../store";
import { updateSearchText } from "../store/searchSlice";

const drawerWidth = 240;

function SideNav({ children }: { children: React.ReactNode }) {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [isClosing, setIsClosing] = useState(false);
  const [activeIndex, setActiveIndex] = useState(0);
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const dispatch = useDispatch();

  const handleItemClick = (index: number) => {
    setActiveIndex(index);
  };

  const addSentenceToSearch = (text: string) => {
    dispatch(updateSearchText(text));
  };

  const handleDrawerClose = () => {
    setIsClosing(true);
    setMobileOpen(false);
  };

  const handleDrawerTransitionEnd = () => {
    setIsClosing(false);
  };

  const handleDrawerToggle = () => {
    if (!isClosing) {
      setMobileOpen(!mobileOpen);
    }
  };

  const openFile = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!event.target || !event.target.files || event.target.files.length === 0)
      return;

    const file = event.target.files[0];
    try {
      addSentenceToSearch("File is Validating")
      const data = await AddFileAPI(file);
      addSentenceToSearch(data.summary)
      console.log(data);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  const drawer = (
    <div className="mt-14">
      <Toolbar />
      <List>
        <ListItem disablePadding>
          <ListItemButton onClick={openFile}>
            <ListItemIcon>
              <AiFillFileAdd size={30} />
            </ListItemIcon>
            <div className="text-lg font-extrabold">Add File</div>
          </ListItemButton>
        </ListItem>
      </List>
    </div>
  );

  const drawermain = (
    <div className="mb-96 h-full">
      <Toolbar />
      <List>
        {[{ link: "", image: "", title: "" }].map((item, index) => (
          <Link href={item.link} key={index}>
            <ListItem
              disablePadding
              onClick={() => handleItemClick(index)}
              sx={{
                backgroundColor: activeIndex === index ? "transparent" : "transparent",
              }}
            >
              <ListItemButton>
                <ListItemIcon>
                  {item.image && <item.image size={30} />}
                </ListItemIcon>
                <div className="text-lg font-extrabold">{item.title}</div>
              </ListItemButton>
            </ListItem>
          </Link>
        ))}
      </List>
    </div>
  );

  const darkTheme = createTheme({
    palette: {
      mode: "dark",
      background: {
        default: "#121212",
        paper: "#121212",
      },
    },
    components: {
      MuiAppBar: {
        styleOverrides: {
          root: {
            backgroundColor: "#000",
          },
        },
      },
    },
  });

  return (
    <ThemeProvider theme={darkTheme}>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <Box
          component="nav"
          sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
          aria-label="mailbox folders"
        >
          <Drawer
            variant="temporary"
            open={mobileOpen}
            onTransitionEnd={handleDrawerTransitionEnd}
            onClose={handleDrawerClose}
            ModalProps={{
              keepMounted: true,
            }}
            sx={{
              display: { xs: "block", sm: "none" },
              "& .MuiDrawer-paper": {
                boxSizing: "border-box",
                width: drawerWidth,
              },
            }}
          >
            {drawer}
          </Drawer>
          <Drawer
            variant="permanent"
            sx={{
              display: { xs: "none", sm: "block" },
              "& .MuiDrawer-paper": {
                boxSizing: "border-box",
                width: drawerWidth,
              },
            }}
            open
          >
            {drawermain}
            {drawer}
          </Drawer>
        </Box>
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3,
            width: { sm: `calc(100% - ${drawerWidth}px)` },
            height: "100vh",
            backgroundImage: "url(https://wallpapers.com/images/featured/plain-black-background-02fh7564l8qq4m6d.jpg)",
            backgroundSize: "cover",
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
          }}
        >
          <div className="font-extrabold text-xl md:text-3xl from-neutral-50 border-b-2 pb-4">
            Aventus
          </div>
          {children}
        </Box>
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: "none" }}
          onChange={handleFileChange}
        />
      </Box>
    </ThemeProvider>
  );
}

export default function App({ children }: { children: React.ReactNode }) {
  return (
    <Provider store={store}>
      <SideNav>{children}</SideNav>
    </Provider>
  );
}
