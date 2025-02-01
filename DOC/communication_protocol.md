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

### Block Check Character (BCC)
BCC is calculated as the XOR of all preceding bytes in the packet (excluding the BCC field itself). This ensures data integrity.

---

## Commands and Sequences

### Command: Encrypt
#### Description
This command encrypts the data sent by the PC and returns the encrypted data.

| Direction  | Command | Size | Data        | BCC  | Response         |
|------------|---------|------|-------------|------|------------------|
| PC → STM   | `0x01`  | xx   | Plain data  | BCC  | -                |
| STM → PC   | `0x01`  | yy   | Encrypted data | BCC | Correct/Incorrect BCC |

#### Error Handling
- If the BCC is incorrect, STM32 responds with `0xFF` and does not process the request.

---

### Command: Decrypt
#### Description
This command decrypts the data sent by the PC and returns the plain text data.

| Direction  | Command | Size | Data            | BCC  | Response         |
|------------|---------|------|-----------------|------|------------------|
| PC → STM   | `0x02`  | xx   | Encrypted data  | BCC  | -                |
| STM → PC   | `0x02`  | yy   | Decrypted data  | BCC  | Correct/Incorrect BCC |

#### Error Handling
- If the BCC is incorrect, STM32 responds with `0xFF`.

---

## Example Communication Sequences

### Example 1: Encrypt
#### PC → STM32
- **Command:** `0x45`
- **Size:** `0x05`
- **Data:** `[0x89, 0x23, 0x7A, 0x56, 0x41]` (encrypted data)
- **BCC:** `0x37` (calculated XOR)

#### STM32 → PC
- **Command:** `0x01`
- **Size:** `0x05`
- **Data:** `[0x89, 0x23, 0x7A, 0x56, 0x41]` (encrypted data)
- **BCC:** `0x37` (calculated XOR)

---

### Example 2: Decrypt
#### PC → STM32
- **Command:** `0x44`
- **Size:** `0x05` (5 bytes of data)
- **Data:** `[0x89, 0x23, 0x7A, 0x56, 0x41]` (encrypted data)
- **BCC:** `0x37`

#### STM32 → PC
- **Command:** `0x02`
- **Size:** `0x05`
- **Data:** `[0xAB, 0xCD, 0xEF, 0x12, 0x34]` (decrypted data)
- **BCC:** `0x98`

---

## Error Handling
1. **Incorrect BCC:**
   - If the BCC check fails, STM32 responds with:
     - **Command:** `0xFF`
     - **Size:** `0x00`
     - **Data:** `None`
     - **BCC:** `0xFF`
2. **Timeouts:**
- If no response is received within a predefined timeout, the PC retries the command.

---


