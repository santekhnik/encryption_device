# Communication Protocol for PC-STM32

## Overview

This document describes the commands and communication sequences used for data exchange between a PC and STM32.

## Command Types

1. **Encrypt**
2. **Decrypt**

---

## Communication Format

### General Packet Structure
Each communication packet follows the structure below:

| Field Name  | Description                                |
|-------------|--------------------------------------------|
| Command     | Command identifier (1 byte).              |
| Size        | Size of the data block (1 byte).          |
| Data        | The actual payload data (variable size).  |
| BCC         | Block Check Character for error detection (1 byte). |





