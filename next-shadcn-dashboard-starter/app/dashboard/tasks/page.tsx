"use client"
import { CellAction } from './_components/task-tables/cell-action';
import * as React from "react"
import {
  ColumnDef,
  ColumnFiltersState,
  SortingState,
  VisibilityState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table"
import { ArrowUpDown, ChevronDown, MoreHorizontal } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import PageContainer from "@/components/layout/page-container"
import { Task } from "@/constants/data"
import { useEffect, useState } from "react"
import { toast } from 'sonner';
import { Modal } from '@/components/ui/modal';
import { DialogContent, DialogTitle } from '@radix-ui/react-dialog';
import { X } from 'lucide-react';

// const data: Payment[] = [
//   {
//     id: "m5gr84i9",
//     amount: 316,
//     status: "success",
//     email: "ken99@yahoo.com",
//   },
//   {
//     id: "3u1reuv4",
//     amount: 242,
//     status: "success",
//     email: "Abe45@gmail.com",
//   },
//   {
//     id: "derv1ws0",
//     amount: 837,
//     status: "processing",
//     email: "Monserrat44@gmail.com",
//   },
//   {
//     id: "5kma53ae",
//     amount: 874,
//     status: "success",
//     email: "Silas22@gmail.com",
//   },
//   {
//     id: "bhqecj4p",
//     amount: 721,
//     status: "failed",
//     email: "carmella@hotmail.com",
//   },
//   {
//     id: "derv1ws0",
//     amount: 837,
//     status: "processing",
//     email: "Monserrat44@gmail.com",
//   },
//   {
//     id: "5kma53ae",
//     amount: 874,
//     status: "success",
//     email: "Silas22@gmail.com",
//   },
//   {
//     id: "bhqecj4p",
//     amount: 721,
//     status: "failed",
//     email: "carmella@hotmail.com",
//   },
//   {
//     id: "derv1ws0",
//     amount: 837,
//     status: "processing",
//     email: "Monserrat44@gmail.com",
//   },
//   {
//     id: "5kma53ae",
//     amount: 874,
//     status: "success",
//     email: "Silas22@gmail.com",
//   },
//   {
//     id: "bhqecj4p",
//     amount: 721,
//     status: "failed",
//     email: "carmella@hotmail.com",
//   },
//   {
//     id: "derv1ws0",
//     amount: 837,
//     status: "processing",
//     email: "Monserrat44@gmail.com",
//   },
//   {
//     id: "5kma53ae",
//     amount: 874,
//     status: "success",
//     email: "Silas22@gmail.com",
//   },
//   {
//     id: "bhqecj4p",
//     amount: 721,
//     status: "failed",
//     email: "carmella@hotmail.com",
//   },
//   {
//     id: "derv1ws0",
//     amount: 837,
//     status: "processing",
//     email: "Monserrat44@gmail.com",
//   },
//   {
//     id: "5kma53ae",
//     amount: 874,
//     status: "success",
//     email: "Silas22@gmail.com",
//   },
//   {
//     id: "bhqecj4p",
//     amount: 721,
//     status: "failed",
//     email: "carmella@hotmail.com",
//   },
//   {
//     id: "derv1ws0",
//     amount: 837,
//     status: "processing",
//     email: "Monserrat44@gmail.com",
//   },
//   {
//     id: "5kma53ae",
//     amount: 874,
//     status: "success",
//     email: "Silas22@gmail.com",
//   },
//   {
//     id: "bhqecj4p",
//     amount: 721,
//     status: "failed",
//     email: "carmella@hotmail.com",
//   },
//   {
//     id: "derv1ws0",
//     amount: 837,
//     status: "processing",
//     email: "Monserrat44@gmail.com",
//   },
//   {
//     id: "5kma53ae",
//     amount: 874,
//     status: "success",
//     email: "Silas22@gmail.com",
//   },
//   {
//     id: "bhqecj4p",
//     amount: 721,
//     status: "failed",
//     email: "carmella@hotmail.com",
//   },
// ]

// export type Payment = {
//   id: string
//   amount: number
//   status: "pending" | "processing" | "success" | "failed"
//   email: string
// }

export const columns: ColumnDef<Task>[] = [
  {
    id: "select",
    header: ({ table }) => (
      <Checkbox
        checked={
          table.getIsAllPageRowsSelected() ||
          (table.getIsSomePageRowsSelected() && "indeterminate")
        }
        onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
        aria-label="Select all"
      />
    ),
    cell: ({ row }) => (
      <Checkbox
        checked={row.getIsSelected()}
        onCheckedChange={(value) => row.toggleSelected(!!value)}
        aria-label="Select row"
      />
    ),
    enableSorting: false,
    enableHiding: false,
  },
  // {
  //   accessorKey: "ID",
  //   header: "id",
  //   cell: ({ row }) => row.getValue("id")
  // },
  {
    accessorKey: "id",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          ID
          <ArrowUpDown />
        </Button>
      )
    },
    cell: ({ row }) => <div className="lowercase">{row.getValue("id")}</div>,
  },
  {
    accessorKey: "title",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Title
          <ArrowUpDown />
        </Button>
      )
    },
    cell: ({ row }) => <div className="lowercase">{row.getValue("title")}</div>,
  },
  {
    accessorKey: "workItemType",
    header: "Type",
    cell: ({ row }) => row.getValue("workItemType")
  },
  {
    accessorKey: "state",
    header: "State",
    cell: ({ row }) => row.getValue("state")
  },
  {
    id: 'actions',
    cell: ({ row }) => <CellAction data={row.original} />
  }
  
  // {
  //   accessorKey: "amount",
  //   header: () => <div className="text-right">Amount</div>,
  //   cell: ({ row }) => {
  //     const amount = parseFloat(row.getValue("amount"))

  //     // Format the amount as a dollar amount
  //     const formatted = new Intl.NumberFormat("en-US", {
  //       style: "currency",
  //       currency: "USD",
  //     }).format(amount)

  //     return <div className="text-right font-medium">{formatted}</div>
  //   },
  // },
  
  // {
  //   id: "actions",
  //   enableHiding: false,
  //   cell: ({ row }) => {
  //     const payment = row.original

  //     return (
  //       <DropdownMenu>
  //         <DropdownMenuTrigger asChild>
  //           <Button variant="ghost" className="h-8 w-8 p-0">
  //             <span className="sr-only">Open menu</span>
  //             <MoreHorizontal />
  //           </Button>
  //         </DropdownMenuTrigger>
  //         <DropdownMenuContent align="end">
  //           <DropdownMenuLabel>Actions</DropdownMenuLabel>
  //           <DropdownMenuItem
  //             onClick={() => navigator.clipboard.writeText(payment.id)}
  //           >
  //             Copy payment ID
  //           </DropdownMenuItem>
  //           <DropdownMenuSeparator />
  //           <DropdownMenuItem>View customer</DropdownMenuItem>
  //           <DropdownMenuItem>View payment details</DropdownMenuItem>
  //         </DropdownMenuContent>
  //       </DropdownMenu>
  //     )
  //   },
  // },
]

export default function DataTableDemo() {

  const [tasks, setTasks] = useState<Task[]>([]);
  const [sorting, setSorting] = React.useState<SortingState>([])
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    []
  )
  const [columnVisibility, setColumnVisibility] =
    React.useState<VisibilityState>({})
  const [rowSelection, setRowSelection] = React.useState({})
  const [idsArray, setIdsArray] = useState([]);
  const [responseData, setResponseData] = useState<{ [key: string]: string }[] | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const handleButtonClick = () => {
    const filteredRows = table.getFilteredSelectedRowModel().rows;
  
    if (filteredRows.length > 0) {
      // Extract IDs from selected rows
      const taskIds = filteredRows.map((row) => row.original.id);
  
      // Send POST request using Fetch API
      fetch('http://127.0.0.1:5000/api/status_report/generate_gpt_task_assignment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          task_ids: taskIds, // Send the array of IDs
        }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          console.log(response.json)
          return response.json();
        })
        .then((data) => {
          setResponseData(data); 
          setIsModalOpen(true);
          toast.success('Task assignment generated successfully!');
          console.log('Success:', data);
        })
        .catch((error) => {
          toast.error('Error generating task assignments');
          console.error('Error:', error);
        });
    } else {
      toast.error('Please select at least one item to assign.');
    }
  };
  
  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await fetch(
          'http://127.0.0.1:5000/api/automated_task_assignment/fetch_unassigned_tasks'
        );
        const data = await response.json();

        const fetchedTasks = data.workItems.map((item: any) => ({
          id: item.id,
          url: item.url,
          workItemType: item.fields['System.WorkItemType'],
          state: item.fields['System.State'],
          title: item.fields['System.Title']
        }));

        setTasks(fetchedTasks);
      } catch (error) {
        console.error('Error fetching tasks:', error);
      }
    };

    fetchTasks();
  }, []);
  const removeTask = async (taskId: string) => {
    try {
      setResponseData((prevData) =>
      prevData ? prevData.filter((task) => !task.hasOwnProperty(taskId)) : []
      );
    } catch (error) {
      toast.error(`Error removing task: ${String(error)}`);
    }
  }
  
  const assignTask = async (taskId: string, email: string) => {
    console.log("clicked");
    try {
      const url = `http://127.0.0.1:5000/api/automated_task_assignment/update_work_item/${taskId}/${email}`;
      const response = await fetch(url, {
        method: 'POST',
        mode: 'cors',
      });

      if (response.ok) {
        toast.success(`Task successfully assigned to ${email}`);
        console.log(`Task assigned to ${email}`);
        setResponseData((prevData) =>
          prevData ? prevData.filter((task) => !task.hasOwnProperty(taskId)) : []
        );
      } else {
        console.error('Failed to assign task');
      }
    } catch (error) {
      console.error('Error assigning task:', error);
    }
  };

  
  const assignAllTasks = async () => {
    try {
      if (responseData) {
        // Prepare the data as an array of { taskId, email } objects
        const tasksToAssign = responseData.map((task: { [key: string]: string }) => {
          const taskId = Object.keys(task)[0];
          const taskAssignments = JSON.parse(task[taskId]).assignments;
          const email = taskAssignments[0]?.email;
  
          return { taskId, email };
        });
  
        // Send a single POST request to the bulk update API
        const response = await fetch('http://127.0.0.1:5000/api/automated_task_assignment/bulk_update', {
          method: 'POST',
          mode: 'cors',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(tasksToAssign),
        });
  
        if (response.ok) {
          const result = await response.json();
          console.log('Bulk assignment result:', result);
          toast.success('All tasks successfully assigned');
          setResponseData([]);
          
        } else {
          console.error('Failed to assign tasks in bulk');
          toast.error('Error assigning all tasks');
        }
      }
    } catch (error) {
      console.error('Error assigning tasks:', error);
      toast.error('Error assigning all tasks');
    }
  };

  const table = useReactTable({
    data:tasks,
    columns,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    onRowSelectionChange: setRowSelection,
    state: {
      sorting,
      columnFilters,
      columnVisibility,
      rowSelection,
    },
  })
  
  return (
    <PageContainer>
    <div className="w-full text-black">
      <div className="flex items-around justify-between py-4">
        <Input
          placeholder="Search Tasks..."
          value={(table.getColumn("title")?.getFilterValue() as string) ?? ""}
          onChange={(event) =>
            table.getColumn("title")?.setFilterValue(event.target.value)
          }
          className="max-w-sm"
        />
        <div>
        {/* <DropdownMenu >
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="ml-auto">
              Columns <ChevronDown />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            {table
              .getAllColumns()
              .filter((column) => column.getCanHide())
              .map((column) => {
                return (
                  <DropdownMenuCheckboxItem
                    key={column.id}
                    className="capitalize"
                    checked={column.getIsVisible()}
                    onCheckedChange={(value) =>
                      column.toggleVisibility(!!value)
                    }
                  >
                    {column.id}
                  </DropdownMenuCheckboxItem>
                )
              })}
          </DropdownMenuContent>
        </DropdownMenu> */}
        <Button  className="mx-2 ml-auto" onClick={handleButtonClick}>
              Ask AI to assign 
        </Button>
        </div>
      </div>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                    </TableHead>
                  )
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && "selected"}
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <div className="flex items-center justify-end space-x-2 py-4">
        <div className="flex-1 text-sm text-muted-foreground">
          {table.getFilteredSelectedRowModel().rows.length} of{" "}
          {table.getFilteredRowModel().rows.length} row(s) selected.
        </div>
        <div className="space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
          >
            Previous
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
          >
            Next
          </Button>
        </div>
      </div>
    </div>
    <div>
      {/* {table.getFilteredSelectedRowModel().rows.map((row) => (
        // <div className='text-black' key={row.id}>{row.original.id}</div>
        
      ))} */}
    </div>
    
    <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title={''}>
        <h1>Task Assignments</h1>
        
          {responseData && responseData.length > 0 ? (
            <div className="mt-4 text-black mx-auto p-6">
              <table>
                <thead>
                  <tr>
                    <th>Task ID</th>
                    <th>User Email</th>
                    <th>Reason</th>
                  </tr>
                </thead>
                <tbody>
                  {responseData.map((task: { [key: string]: string }, index: number) => {
                    const taskId = Object.keys(task)[0];
                    const taskAssignments = JSON.parse(task[taskId]).assignments;

                    return (
                      <tr key={index}>
                        <td className='p-2'>{taskId}</td>
                        <td className='p-2'>{taskAssignments[0]?.email}</td>
                        <td className='p-2'>{taskAssignments[0]?.reason}</td>
                        <td className='p-2'>
                          <Button onClick={() => assignTask(taskId, taskAssignments[0]?.email)}>
                            <div className='p-2 text-nowrap'>Confirm AI suggestions</div>
                          </Button>
                        </td>
                        <td className='p-2'>
                          <X role='button' onClick={() => removeTask(taskId)} />
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          ) : (
            
              <div  className='p-2 w-full text-center'>No tasks left</div>
            
          )}
        
        <Button
          className="p-2 mx-2"
          onClick={() => assignAllTasks()}
        >
          Assign All Tasks
        </Button>

        <Button className='mx-2' variant={'outline'} onClick={() => setIsModalOpen(false)}>Close</Button>

      </Modal>
      


    </PageContainer>
  )
  // const idsArray = table.getFilteredSelectedRowModel().rows.map((row) => row.original.id);
}
